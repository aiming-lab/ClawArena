"""JS 子集的异步树遍历解释器（与 SMbench 无耦合的纯执行引擎）。

被测 main agent 提交的 Workflow 脚本是 JS 语法。由于 SMbench **不运行真 JS**，而是
把脚本解析为 AST 后在 Python 里解释执行，从而让编排原语直接调用现有
``SubagentManager``、复用全部生命周期统计。

解析器用 ``esprima``（支持 ES2017：箭头函数、模板串、for-of、解构、spread、
async/await）。脚本体在解析前去掉 ``export`` 并包进一个 ``async function``，以支持
脚本顶层 ``await`` 与脚本末尾 ``return``。

支持的 JS 子集（够覆盖 claude-code workflow 文档里的全部编排模式）：
- 声明：``const`` / ``let`` / ``var``；简单解构（数组 / 对象 pattern）。
- 控制流：``if/else``、``for`` (C 式)、``for...of``、``while``、``break``/``continue``、``return``。
- 表达式：字面量、模板串、数组 / 对象字面量、成员访问、调用、箭头 / 函数表达式、
  一元 / 二元 / 逻辑 / 三元 / 赋值 / 自增自减、``await``、spread。
- 内建：``Math`` / ``JSON`` / ``Object`` / ``Array`` / ``console`` 的常用方法，以及
  数组 / 字符串的常用方法（map/filter/forEach/flat/flatMap/push/slice/concat/join/
  includes/find/some/every/reduce/sort/keys/length 等）。

**Promise 模型（务实简化）**：调用点自动 resolve——异步内建（agent/parallel/pipeline/
workflow）在 CallExpression 处即被 ``await``，函数调用（``invoke_fn``）跑到底返回其值。
并发**只**来自 ``parallel()`` / ``pipeline()``（内部用 ``asyncio.gather`` 真并发地驱动
各 thunk / stage）。因此「先存若干 promise 再一起 await」的非惯用写法会退化为串行
（结果仍正确，仅并发度降低）——文档已引导用 parallel/pipeline 取得并发。
"""
from __future__ import annotations

import asyncio
import json as _json
import math
from dataclasses import dataclass, field
from typing import Any

import esprima

from .errors import WorkflowScriptError


# ---------------------------------------------------------------------------
# 控制流信号
# ---------------------------------------------------------------------------
class _Return(Exception):
    def __init__(self, value: Any):
        self.value = value


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


# JS undefined 的 Python 表示。用单例与 None(=JS null) 区分；但二者在 Python 层
# 多数运算等价，falsy 判定相同。
class _Undefined:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
        return cls._inst

    def __repr__(self):
        return "undefined"

    def __bool__(self):
        return False


UNDEFINED = _Undefined()


# ---------------------------------------------------------------------------
# Scope / 函数值
# ---------------------------------------------------------------------------
class Scope:
    __slots__ = ("vars", "parent")

    def __init__(self, parent: "Scope | None" = None):
        self.vars: dict[str, Any] = {}
        self.parent = parent

    def lookup_scope(self, name: str) -> "Scope | None":
        s: Scope | None = self
        while s is not None:
            if name in s.vars:
                return s
            s = s.parent
        return None

    def get(self, name: str) -> Any:
        s = self.lookup_scope(name)
        if s is None:
            raise WorkflowScriptError(f"undefined variable: {name}")
        return s.vars[name]

    def has(self, name: str) -> bool:
        return self.lookup_scope(name) is not None

    def declare(self, name: str, value: Any) -> None:
        self.vars[name] = value

    def assign(self, name: str, value: Any) -> None:
        s = self.lookup_scope(name)
        if s is None:
            # 赋值未声明变量：落到当前作用域（宽松，避免脚本小错直接崩）。
            self.vars[name] = value
        else:
            s.vars[name] = value


@dataclass
class JsFunction:
    params: list
    body: Any
    is_expr: bool  # 箭头表达式体（隐式 return）
    closure: Scope
    name: str = "<anon>"


# ---------------------------------------------------------------------------
# JS 语义辅助
# ---------------------------------------------------------------------------
def js_truthy(v: Any) -> bool:
    if v is UNDEFINED or v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0 and not (isinstance(v, float) and math.isnan(v))
    if isinstance(v, str):
        return len(v) > 0
    return True


def js_to_str(v: Any) -> str:
    if v is UNDEFINED:
        return "undefined"
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return repr(v)
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return ",".join(js_to_str(x) for x in v)
    if isinstance(v, dict):
        return "[object Object]"
    if isinstance(v, JsFunction):
        return f"function {v.name}"
    return str(v)


def js_to_num(v: Any) -> float:
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return 0.0
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return 0.0
        try:
            return float(s)
        except ValueError:
            return float("nan")
    return float("nan")


def _strict_eq(a: Any, b: Any) -> bool:
    # === ：类型也要一致（bool 与 number 在 Python 里 1==True，需区分）。
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if (a is UNDEFINED) or (b is UNDEFINED):
        return a is b
    if a is None or b is None:
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return float(a) == float(b)
    if type(a) is type(b):
        return a == b
    return False


def _loose_eq(a: Any, b: Any) -> bool:
    if (a is UNDEFINED or a is None) and (b is UNDEFINED or b is None):
        return True
    if _strict_eq(a, b):
        return True
    if isinstance(a, (int, float)) and isinstance(b, str):
        return float(a) == js_to_num(b)
    if isinstance(a, str) and isinstance(b, (int, float)):
        return js_to_num(a) == float(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return js_to_num(a) == js_to_num(b)
    return False


def _t(node: Any) -> str:
    return getattr(node, "type", "")


# ---------------------------------------------------------------------------
# 解释器
# ---------------------------------------------------------------------------
class Interpreter:
    def __init__(self, builtins: dict[str, Any], *, max_calls: int = 100000):
        self.builtins = builtins
        self._call_count = 0
        self._max_calls = max_calls

    # ---- 入口 ----
    @staticmethod
    def parse(source: str):
        """去掉 ``export`` 并包进 async function，返回其 BlockStatement body 节点。"""
        stripped = source.replace("export const", "const").replace(
            "export default", ""
        ).replace("export ", "")
        wrapped = "async function __wf__() {\n" + stripped + "\n}"
        try:
            tree = esprima.parseScript(wrapped, {"tolerant": True})
        except Exception as e:  # noqa: BLE001
            raise WorkflowScriptError(f"script parse error: {e}") from e
        fn = tree.body[0]
        if _t(fn) != "FunctionDeclaration":
            raise WorkflowScriptError("internal: wrapper is not a FunctionDeclaration")
        return fn.body  # BlockStatement

    async def run(self, source: str, global_vars: dict[str, Any]) -> Any:
        block = self.parse(source)
        root = Scope()
        for k, v in self.builtins.items():
            root.declare(k, v)
        for k, v in global_vars.items():
            root.declare(k, v)
        try:
            await self.exec_block(block, root, new_scope=False)
        except _Return as r:
            return r.value
        return UNDEFINED

    # ---- 语句 ----
    async def exec_block(self, block: Any, scope: Scope, *, new_scope: bool = True) -> None:
        inner = Scope(scope) if new_scope else scope
        for stmt in block.body:
            await self.exec_stmt(stmt, inner)

    async def exec_stmt(self, node: Any, scope: Scope) -> None:
        t = _t(node)
        if t == "VariableDeclaration":
            for decl in node.declarations:
                init = await self.eval(decl.init, scope) if decl.init is not None else UNDEFINED
                await self._bind_pattern(decl.id, init, scope, declare=True)
        elif t == "ExpressionStatement":
            await self.eval(node.expression, scope)
        elif t == "ReturnStatement":
            val = await self.eval(node.argument, scope) if node.argument is not None else UNDEFINED
            raise _Return(val)
        elif t == "IfStatement":
            if js_truthy(await self.eval(node.test, scope)):
                await self.exec_stmt(node.consequent, scope)
            elif node.alternate is not None:
                await self.exec_stmt(node.alternate, scope)
        elif t == "BlockStatement":
            await self.exec_block(node, scope)
        elif t == "ForStatement":
            await self._exec_for(node, scope)
        elif t == "ForOfStatement":
            await self._exec_for_of(node, scope)
        elif t == "WhileStatement":
            while js_truthy(await self.eval(node.test, scope)):
                try:
                    await self.exec_stmt(node.body, scope)
                except _Break:
                    break
                except _Continue:
                    continue
        elif t == "BreakStatement":
            raise _Break()
        elif t == "ContinueStatement":
            raise _Continue()
        elif t == "FunctionDeclaration":
            scope.declare(node.id.name, self._make_function(node, scope))
        elif t == "EmptyStatement":
            return
        else:
            raise WorkflowScriptError(f"unsupported statement: {t}")

    async def _exec_for(self, node: Any, scope: Scope) -> None:
        loop = Scope(scope)
        if node.init is not None:
            if _t(node.init) == "VariableDeclaration":
                await self.exec_stmt(node.init, loop)
            else:
                await self.eval(node.init, loop)
        while node.test is None or js_truthy(await self.eval(node.test, loop)):
            try:
                await self.exec_stmt(node.body, loop)
            except _Break:
                break
            except _Continue:
                pass
            if node.update is not None:
                await self.eval(node.update, loop)

    async def _exec_for_of(self, node: Any, scope: Scope) -> None:
        iterable = await self.eval(node.right, scope)
        items = self._iter(iterable)
        for item in items:
            loop = Scope(scope)
            left = node.left
            if _t(left) == "VariableDeclaration":
                await self._bind_pattern(left.declarations[0].id, item, loop, declare=True)
            else:
                await self._bind_pattern(left, item, loop, declare=False)
            try:
                await self.exec_stmt(node.body, loop)
            except _Break:
                break
            except _Continue:
                continue

    def _iter(self, v: Any):
        if isinstance(v, list):
            return list(v)
        if isinstance(v, str):
            return list(v)
        if isinstance(v, dict):
            return list(v.keys())
        if v is UNDEFINED or v is None:
            return []
        raise WorkflowScriptError(f"value is not iterable: {type(v).__name__}")

    # ---- 解构 / 绑定 ----
    async def _bind_pattern(self, target: Any, value: Any, scope: Scope, *, declare: bool) -> None:
        t = _t(target)
        if t == "Identifier":
            if declare:
                scope.declare(target.name, value)
            else:
                scope.assign(target.name, value)
        elif t == "ArrayPattern":
            seq = value if isinstance(value, list) else self._iter(value)
            for i, el in enumerate(target.elements):
                if el is None:
                    continue
                if _t(el) == "RestElement":
                    await self._bind_pattern(el.argument, list(seq[i:]), scope, declare=declare)
                    break
                v = seq[i] if i < len(seq) else UNDEFINED
                if _t(el) == "AssignmentPattern":
                    if v is UNDEFINED:
                        v = await self.eval(el.right, scope)
                    await self._bind_pattern(el.left, v, scope, declare=declare)
                else:
                    await self._bind_pattern(el, v, scope, declare=declare)
        elif t == "ObjectPattern":
            obj = value if isinstance(value, dict) else {}
            for prop in target.properties:
                if _t(prop) == "RestElement":
                    continue  # 对象 rest 暂不支持，忽略
                key = prop.key.name if _t(prop.key) == "Identifier" else await self.eval(prop.key, scope)
                v = obj.get(key, UNDEFINED) if isinstance(obj, dict) else UNDEFINED
                tgt = prop.value
                if _t(tgt) == "AssignmentPattern":
                    if v is UNDEFINED:
                        v = await self.eval(tgt.right, scope)
                    await self._bind_pattern(tgt.left, v, scope, declare=declare)
                else:
                    await self._bind_pattern(tgt, v, scope, declare=declare)
        else:
            raise WorkflowScriptError(f"unsupported binding pattern: {t}")

    def _make_function(self, node: Any, scope: Scope) -> JsFunction:
        is_expr = _t(node) == "ArrowFunctionExpression" and bool(getattr(node, "expression", False))
        name = node.id.name if getattr(node, "id", None) else "<anon>"
        return JsFunction(params=list(node.params), body=node.body, is_expr=is_expr, closure=scope, name=name)

    async def invoke_fn(self, fn: JsFunction, args: list[Any]) -> Any:
        self._call_count += 1
        if self._call_count > self._max_calls:
            raise WorkflowScriptError("interpreter call budget exceeded (possible runaway loop)")
        call_scope = Scope(fn.closure)
        for i, p in enumerate(fn.params):
            if _t(p) == "RestElement":
                await self._bind_pattern(p.argument, list(args[i:]), call_scope, declare=True)
                break
            v = args[i] if i < len(args) else UNDEFINED
            if _t(p) == "AssignmentPattern":
                if v is UNDEFINED:
                    v = await self.eval(p.right, call_scope)
                await self._bind_pattern(p.left, v, call_scope, declare=True)
            else:
                await self._bind_pattern(p, v, call_scope, declare=True)
        if fn.is_expr:
            return await self.eval(fn.body, call_scope)
        try:
            await self.exec_block(fn.body, call_scope, new_scope=False)
        except _Return as r:
            return r.value
        return UNDEFINED

    # ---- 表达式 ----
    async def eval(self, node: Any, scope: Scope) -> Any:
        t = _t(node)
        m = getattr(self, f"_e_{t}", None)
        if m is None:
            raise WorkflowScriptError(f"unsupported expression: {t}")
        return await m(node, scope)

    async def _e_Literal(self, node: Any, scope: Scope) -> Any:
        # esprima：number→int/float、string→str、true/false→bool、null→None。
        return node.value

    async def _e_Identifier(self, node: Any, scope: Scope) -> Any:
        name = node.name
        if name == "undefined":
            return UNDEFINED
        if not scope.has(name):
            return UNDEFINED
        return scope.get(name)

    async def _e_TemplateLiteral(self, node: Any, scope: Scope) -> Any:
        out: list[str] = []
        quasis = node.quasis
        exprs = node.expressions
        for i, q in enumerate(quasis):
            out.append(q.value.cooked or "")
            if i < len(exprs):
                out.append(js_to_str(await self.eval(exprs[i], scope)))
        return "".join(out)

    async def _e_ArrayExpression(self, node: Any, scope: Scope) -> Any:
        out: list[Any] = []
        for el in node.elements:
            if el is None:
                out.append(UNDEFINED)
            elif _t(el) == "SpreadElement":
                out.extend(self._iter(await self.eval(el.argument, scope)))
            else:
                out.append(await self.eval(el, scope))
        return out

    async def _e_ObjectExpression(self, node: Any, scope: Scope) -> Any:
        obj: dict[str, Any] = {}
        for prop in node.properties:
            if _t(prop) == "SpreadElement":
                src = await self.eval(prop.argument, scope)
                if isinstance(src, dict):
                    obj.update(src)
                continue
            if getattr(prop, "computed", False):
                key = js_to_str(await self.eval(prop.key, scope))
            else:
                k = prop.key
                key = k.name if _t(k) == "Identifier" else js_to_str(k.value)
            obj[key] = await self.eval(prop.value, scope)
        return obj

    async def _e_ArrowFunctionExpression(self, node: Any, scope: Scope) -> Any:
        return self._make_function(node, scope)

    async def _e_FunctionExpression(self, node: Any, scope: Scope) -> Any:
        return self._make_function(node, scope)

    async def _e_AwaitExpression(self, node: Any, scope: Scope) -> Any:
        val = await self.eval(node.argument, scope)
        if asyncio.iscoroutine(val):
            return await val
        return val

    async def _e_UnaryExpression(self, node: Any, scope: Scope) -> Any:
        op = node.operator
        if op == "typeof":
            try:
                v = await self.eval(node.argument, scope)
            except WorkflowScriptError:
                return "undefined"
            return self._typeof(v)
        v = await self.eval(node.argument, scope)
        if op == "!":
            return not js_truthy(v)
        if op == "-":
            return -js_to_num(v)
        if op == "+":
            return js_to_num(v)
        if op == "void":
            return UNDEFINED
        raise WorkflowScriptError(f"unsupported unary operator: {op}")

    def _typeof(self, v: Any) -> str:
        if v is UNDEFINED:
            return "undefined"
        if v is None:
            return "object"
        if isinstance(v, bool):
            return "boolean"
        if isinstance(v, (int, float)):
            return "number"
        if isinstance(v, str):
            return "string"
        if isinstance(v, JsFunction) or callable(v):
            return "function"
        return "object"

    async def _e_UpdateExpression(self, node: Any, scope: Scope) -> Any:
        # ++ / -- ：仅支持作用于 Identifier 与简单成员。
        target = node.argument
        old = js_to_num(await self.eval(target, scope))
        new = old + 1 if node.operator == "++" else old - 1
        new_i = int(new) if float(new).is_integer() else new
        await self._assign_to(target, new_i, scope)
        return (int(old) if float(old).is_integer() else old) if not node.prefix else new_i

    async def _e_BinaryExpression(self, node: Any, scope: Scope) -> Any:
        op = node.operator
        left = await self.eval(node.left, scope)
        right = await self.eval(node.right, scope)
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return js_to_str(left) + js_to_str(right)
            if isinstance(left, list) and isinstance(right, list):
                return js_to_str(left) + js_to_str(right)
            return self._num_result(js_to_num(left) + js_to_num(right))
        if op == "-":
            return self._num_result(js_to_num(left) - js_to_num(right))
        if op == "*":
            return self._num_result(js_to_num(left) * js_to_num(right))
        if op == "/":
            return self._num_result(js_to_num(left) / js_to_num(right)) if js_to_num(right) != 0 else float("inf")
        if op == "%":
            r = js_to_num(right)
            return self._num_result(math.fmod(js_to_num(left), r)) if r != 0 else float("nan")
        if op == "**":
            return self._num_result(js_to_num(left) ** js_to_num(right))
        if op == "===":
            return _strict_eq(left, right)
        if op == "!==":
            return not _strict_eq(left, right)
        if op == "==":
            return _loose_eq(left, right)
        if op == "!=":
            return not _loose_eq(left, right)
        if op in ("<", ">", "<=", ">="):
            return self._compare(left, right, op)
        if op == "instanceof":
            return False
        if op == "in":
            return isinstance(right, dict) and js_to_str(left) in right
        raise WorkflowScriptError(f"unsupported binary operator: {op}")

    @staticmethod
    def _num_result(x: float) -> Any:
        if isinstance(x, float) and x.is_integer():
            return int(x)
        return x

    @staticmethod
    def _compare(left: Any, right: Any, op: str) -> bool:
        if isinstance(left, str) and isinstance(right, str):
            a, b = left, right
        else:
            a, b = js_to_num(left), js_to_num(right)
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        if op == "<=":
            return a <= b
        return a >= b

    async def _e_LogicalExpression(self, node: Any, scope: Scope) -> Any:
        left = await self.eval(node.left, scope)
        op = node.operator
        if op == "&&":
            return (await self.eval(node.right, scope)) if js_truthy(left) else left
        if op == "||":
            return left if js_truthy(left) else (await self.eval(node.right, scope))
        if op == "??":
            return left if (left is not UNDEFINED and left is not None) else (await self.eval(node.right, scope))
        raise WorkflowScriptError(f"unsupported logical operator: {op}")

    async def _e_ConditionalExpression(self, node: Any, scope: Scope) -> Any:
        if js_truthy(await self.eval(node.test, scope)):
            return await self.eval(node.consequent, scope)
        return await self.eval(node.alternate, scope)

    async def _e_AssignmentExpression(self, node: Any, scope: Scope) -> Any:
        op = node.operator
        rhs = await self.eval(node.right, scope)
        if op == "=":
            await self._assign_to(node.left, rhs, scope)
            return rhs
        cur = await self.eval(node.left, scope)
        if op == "+=":
            new = (js_to_str(cur) + js_to_str(rhs)) if (isinstance(cur, str) or isinstance(rhs, str)) else self._num_result(js_to_num(cur) + js_to_num(rhs))
        elif op == "-=":
            new = self._num_result(js_to_num(cur) - js_to_num(rhs))
        elif op == "*=":
            new = self._num_result(js_to_num(cur) * js_to_num(rhs))
        elif op == "/=":
            new = self._num_result(js_to_num(cur) / js_to_num(rhs))
        elif op in ("||=", "&&=", "??="):
            keep = (js_truthy(cur) if op == "&&=" else (not js_truthy(cur)) if op == "||=" else (cur is UNDEFINED or cur is None))
            new = rhs if keep else cur
        else:
            raise WorkflowScriptError(f"unsupported assignment operator: {op}")
        await self._assign_to(node.left, new, scope)
        return new

    async def _assign_to(self, target: Any, value: Any, scope: Scope) -> None:
        t = _t(target)
        if t == "Identifier":
            scope.assign(target.name, value)
        elif t == "MemberExpression":
            obj = await self.eval(target.object, scope)
            key = await self._member_key(target, scope)
            if isinstance(obj, list):
                idx = int(js_to_num(key))
                while len(obj) <= idx:
                    obj.append(UNDEFINED)
                obj[idx] = value
            elif isinstance(obj, dict):
                obj[js_to_str(key)] = value
            else:
                raise WorkflowScriptError("cannot assign to member of non-object")
        elif t in ("ArrayPattern", "ObjectPattern"):
            await self._bind_pattern(target, value, scope, declare=False)
        else:
            raise WorkflowScriptError(f"cannot assign to {t}")

    async def _member_key(self, node: Any, scope: Scope) -> Any:
        if getattr(node, "computed", False):
            return await self.eval(node.property, scope)
        return node.property.name

    async def _e_MemberExpression(self, node: Any, scope: Scope) -> Any:
        obj = await self.eval(node.object, scope)
        key = await self._member_key(node, scope)
        return self._get_member(obj, key)

    def _get_member(self, obj: Any, key: Any) -> Any:
        ks = js_to_str(key)
        if isinstance(obj, _JsSet):
            if ks == "size":
                return len(obj)
            return UNDEFINED
        if isinstance(obj, dict):
            return obj.get(ks, UNDEFINED)
        if isinstance(obj, list):
            if ks == "length":
                return len(obj)
            try:
                idx = int(js_to_num(key))
                return obj[idx] if 0 <= idx < len(obj) else UNDEFINED
            except (ValueError, TypeError):
                return UNDEFINED
        if isinstance(obj, str):
            if ks == "length":
                return len(obj)
            try:
                idx = int(js_to_num(key))
                return obj[idx] if 0 <= idx < len(obj) else UNDEFINED
            except (ValueError, TypeError):
                return UNDEFINED
        if obj is UNDEFINED or obj is None:
            raise WorkflowScriptError(f"cannot read property '{ks}' of {js_to_str(obj)}")
        return UNDEFINED

    async def _e_CallExpression(self, node: Any, scope: Scope) -> Any:
        callee = node.callee
        if _t(callee) == "MemberExpression":
            obj = await self.eval(callee.object, scope)
            method = await self._member_key(callee, scope)
            args = await self._eval_args(node.arguments, scope)
            return await self._call_method(obj, js_to_str(method), args, callee, scope)
        fn = await self.eval(callee, scope)
        args = await self._eval_args(node.arguments, scope)
        return await self.call_value(fn, args)

    async def _e_NewExpression(self, node: Any, scope: Scope) -> Any:
        # 仅支持 new Set() / new Map() 的最小形态（脚本里偶用 Set 去重）。
        callee = node.callee
        name = getattr(callee, "name", "")
        args = await self._eval_args(node.arguments, scope)
        if name == "Set":
            init = args[0] if args else []
            return _JsSet(list(init) if isinstance(init, list) else [])
        if name == "Map":
            return {}
        raise WorkflowScriptError(f"unsupported constructor: new {name}")

    async def _eval_args(self, arg_nodes: list, scope: Scope) -> list[Any]:
        out: list[Any] = []
        for a in arg_nodes:
            if _t(a) == "SpreadElement":
                out.extend(self._iter(await self.eval(a.argument, scope)))
            else:
                out.append(await self.eval(a, scope))
        return out

    async def call_value(self, fn: Any, args: list[Any]) -> Any:
        if isinstance(fn, JsFunction):
            return await self.invoke_fn(fn, args)
        if asyncio.iscoroutinefunction(fn):
            return await fn(*args)
        if callable(fn):
            res = fn(*args)
            if asyncio.iscoroutine(res):
                return await res
            return res
        raise WorkflowScriptError(f"value is not callable: {js_to_str(fn)}")

    async def _call_array_callback(self, fn: Any, args: list[Any]) -> Any:
        return await self.call_value(fn, args)

    # ---- 方法分派（数组 / 字符串 / 命名空间对象）----
    async def _call_method(self, obj: Any, method: str, args: list, callee_node: Any, scope: Scope) -> Any:
        # 命名空间对象（Math / JSON / Object / Array / console）以及 dict 内的函数成员。
        if isinstance(obj, dict):
            member = obj.get(method, UNDEFINED)
            if isinstance(member, JsFunction) or callable(member):
                return await self.call_value(member, args)
            if member is UNDEFINED:
                raise WorkflowScriptError(f"object has no method '{method}'")
            return await self.call_value(member, args)
        if isinstance(obj, _JsSet):
            return obj.method(method, args)
        if isinstance(obj, list):
            return await self._array_method(obj, method, args)
        if isinstance(obj, str):
            return self._string_method(obj, method, args)
        if isinstance(obj, (int, float)):
            return self._number_method(obj, method, args)
        raise WorkflowScriptError(f"cannot call method '{method}' on {self._typeof(obj)}")

    async def _array_method(self, arr: list, method: str, args: list) -> Any:
        if method == "map":
            cb = args[0]
            return [await self._call_array_callback(cb, [x, i, arr]) for i, x in enumerate(arr)]
        if method == "filter":
            cb = args[0]
            out = []
            for i, x in enumerate(arr):
                if js_truthy(await self._call_array_callback(cb, [x, i, arr])):
                    out.append(x)
            return out
        if method == "forEach":
            cb = args[0]
            for i, x in enumerate(arr):
                await self._call_array_callback(cb, [x, i, arr])
            return UNDEFINED
        if method == "find":
            cb = args[0]
            for i, x in enumerate(arr):
                if js_truthy(await self._call_array_callback(cb, [x, i, arr])):
                    return x
            return UNDEFINED
        if method == "findIndex":
            cb = args[0]
            for i, x in enumerate(arr):
                if js_truthy(await self._call_array_callback(cb, [x, i, arr])):
                    return i
            return -1
        if method == "some":
            cb = args[0]
            for i, x in enumerate(arr):
                if js_truthy(await self._call_array_callback(cb, [x, i, arr])):
                    return True
            return False
        if method == "every":
            cb = args[0]
            for i, x in enumerate(arr):
                if not js_truthy(await self._call_array_callback(cb, [x, i, arr])):
                    return False
            return True
        if method == "reduce":
            cb = args[0]
            has_init = len(args) > 1
            acc = args[1] if has_init else UNDEFINED
            start = 0
            if not has_init:
                if not arr:
                    raise WorkflowScriptError("reduce of empty array with no initial value")
                acc = arr[0]
                start = 1
            for i in range(start, len(arr)):
                acc = await self._call_array_callback(cb, [acc, arr[i], i, arr])
            return acc
        if method == "flatMap":
            cb = args[0]
            out: list[Any] = []
            for i, x in enumerate(arr):
                r = await self._call_array_callback(cb, [x, i, arr])
                if isinstance(r, list):
                    out.extend(r)
                else:
                    out.append(r)
            return out
        if method == "flat":
            depth = int(js_to_num(args[0])) if args else 1
            return _flatten(arr, depth)
        if method == "push":
            arr.extend(args)
            return len(arr)
        if method == "pop":
            return arr.pop() if arr else UNDEFINED
        if method == "shift":
            return arr.pop(0) if arr else UNDEFINED
        if method == "unshift":
            for a in reversed(args):
                arr.insert(0, a)
            return len(arr)
        if method == "slice":
            s = int(js_to_num(args[0])) if len(args) > 0 else 0
            e = int(js_to_num(args[1])) if len(args) > 1 else len(arr)
            return arr[s:e]
        if method == "concat":
            out = list(arr)
            for a in args:
                if isinstance(a, list):
                    out.extend(a)
                else:
                    out.append(a)
            return out
        if method == "join":
            sep = js_to_str(args[0]) if args else ","
            return sep.join(js_to_str(x) for x in arr)
        if method == "includes":
            return any(_strict_eq(x, args[0]) for x in arr) if args else False
        if method == "indexOf":
            for i, x in enumerate(arr):
                if _strict_eq(x, args[0]):
                    return i
            return -1
        if method == "sort":
            if args and isinstance(args[0], JsFunction):
                # 比较器需异步调用——用插入排序避免在 cmp 里 await 的复杂度。
                cb = args[0]
                res = list(arr)
                for i in range(1, len(res)):
                    j = i
                    while j > 0:
                        c = js_to_num(await self._call_array_callback(cb, [res[j - 1], res[j]]))
                        if c > 0:
                            res[j - 1], res[j] = res[j], res[j - 1]
                            j -= 1
                        else:
                            break
                arr[:] = res
                return arr
            arr.sort(key=lambda x: (js_to_str(x)))
            return arr
        if method == "reverse":
            arr.reverse()
            return arr
        if method == "keys":
            return list(range(len(arr)))
        raise WorkflowScriptError(f"unsupported array method: {method}")

    def _string_method(self, s: str, method: str, args: list) -> Any:
        if method == "toUpperCase":
            return s.upper()
        if method == "toLowerCase":
            return s.lower()
        if method == "trim":
            return s.strip()
        if method == "split":
            sep = js_to_str(args[0]) if args else None
            return list(s) if sep == "" else (s.split(sep) if sep is not None else [s])
        if method == "slice":
            a = int(js_to_num(args[0])) if len(args) > 0 else 0
            b = int(js_to_num(args[1])) if len(args) > 1 else len(s)
            return s[a:b]
        if method == "substring":
            a = int(js_to_num(args[0])) if len(args) > 0 else 0
            b = int(js_to_num(args[1])) if len(args) > 1 else len(s)
            return s[a:b]
        if method == "includes":
            return js_to_str(args[0]) in s if args else False
        if method == "startsWith":
            return s.startswith(js_to_str(args[0])) if args else False
        if method == "endsWith":
            return s.endswith(js_to_str(args[0])) if args else False
        if method == "replace":
            return s.replace(js_to_str(args[0]), js_to_str(args[1]), 1) if len(args) >= 2 else s
        if method == "replaceAll":
            return s.replace(js_to_str(args[0]), js_to_str(args[1])) if len(args) >= 2 else s
        if method == "repeat":
            return s * int(js_to_num(args[0])) if args else ""
        if method == "padStart":
            return s.rjust(int(js_to_num(args[0])), js_to_str(args[1]) if len(args) > 1 else " ")
        if method == "indexOf":
            return s.find(js_to_str(args[0])) if args else -1
        if method == "toString":
            return s
        raise WorkflowScriptError(f"unsupported string method: {method}")

    def _number_method(self, n: float, method: str, args: list) -> Any:
        if method == "toFixed":
            d = int(js_to_num(args[0])) if args else 0
            return f"{float(n):.{d}f}"
        if method == "toString":
            return js_to_str(n)
        raise WorkflowScriptError(f"unsupported number method: {method}")


def _flatten(arr: list, depth: int) -> list:
    out: list = []
    for x in arr:
        if isinstance(x, list) and depth > 0:
            out.extend(_flatten(x, depth - 1))
        else:
            out.append(x)
    return out


class _JsSet:
    """脚本里 ``new Set()`` 的最小实现（add / has / size / delete + 可迭代）。"""

    def __init__(self, init: list | None = None):
        self._items: list = []
        for x in init or []:
            if not any(_strict_eq(x, y) for y in self._items):
                self._items.append(x)

    def method(self, name: str, args: list) -> Any:
        if name == "add":
            x = args[0]
            if not any(_strict_eq(x, y) for y in self._items):
                self._items.append(x)
            return self
        if name == "has":
            return any(_strict_eq(args[0], y) for y in self._items)
        if name == "delete":
            for i, y in enumerate(self._items):
                if _strict_eq(args[0], y):
                    del self._items[i]
                    return True
            return False
        raise WorkflowScriptError(f"unsupported Set method: {name}")

    def __iter__(self):
        return iter(list(self._items))

    def __len__(self):
        return len(self._items)
