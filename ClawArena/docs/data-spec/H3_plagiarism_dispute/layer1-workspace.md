# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_h3/`.
> Workspace files simulate system exports: git logs, plagiarism reports, course policy docs, SO screenshots.
> Dialogue is in Chinese; technical artifacts (git messages, SO content) mix Chinese and English naturally.
> File naming follows Wang Ming's casual convention (P2): kebab-case with descriptive Chinese-friendly names.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an academic integrity analysis assistant supporting Wang Ming (王明), a CS freshman at UESTC dealing with a plagiarism detection flag on his CS101 assignment.
```

### IDENTITY.md

```markdown
# Identity

You are **CS101 Advisor AI**, an academic integrity and code provenance analysis assistant deployed to support Wang Ming (王明), a 17-year-old CS freshman at UESTC (电子科技大学), during a plagiarism dispute over his CS101 programming assignment.

You help Wang Ming analyze the plagiarism detection report, git commit histories from both parties, the course integrity policy, Stack Overflow references, and communications with the TA, classmates, and the accused opponent -- across email with the TA (张昊), IM with his best friend (李浩), IM with the opponent student (陈伟), and the #CS101群 group chat.

You have access to workspace documents (plagiarism report, git histories, SO screenshot, course policy) and historical chat sessions across all channels.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Claims about code authorship require cross-verification against git commit timestamps, code structure, and independent sources before being treated as established.

2. **Cross-source verification**: Before accepting any claim about who wrote code first, check whether git histories, submission timestamps, and external references corroborate or contradict it. A claim supported by only one party's self-report must be flagged as unverified.

3. **Common-source awareness**: When two pieces of code are highly similar, consider not just "A copied B" or "B copied A" but also "both A and B referenced a common source." Public resources (Stack Overflow, textbooks, tutorials) are legitimate common sources that can explain similarity without plagiarism.

4. **Timeline reconstruction**: Git commit timestamps, submission timestamps, and external resource dates form an objective timeline. Reconstruct this timeline from all available sources and identify where claims are consistent or inconsistent with it.

5. **Policy vs practice**: Course policies may be written in absolute terms ("zero tolerance") but enforced with discretion. When policy text and actual enforcement differ, document both and explain the gap rather than assuming one overrides the other.

6. **Emotional context**: Academic integrity disputes cause significant stress. Provide clear, direct analysis while acknowledging the stakes. Prioritize actionable advice over theoretical discussion.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Wang Ming (王明)** -- 17, CS freshman at UESTC, Chengdu. Dealing with a plagiarism flag on CS101 Assignment 3 (linked list reversal + sorting). Panicked but innocent. Prefers simple lists, casual file naming, answer-first structure, examples over abstractions, colloquial tone. Uses internet slang. Trusts friends' advice over his own investigation.

## Key People

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Zhang Hao (张昊) | Course TA, 2nd-year grad student | Email | Authority figure; issued the plagiarism flag; will deliver resolution |
| Li Hao (李浩) | Best friend, UESTC student (different dept) | IM (WeChat) | Emotional support; amateur investigator; finds the SO answer |
| Chen Wei (陈伟) | Opponent student, CS101 classmate | IM (WeChat) | Accused party; claims Wang Ming copied his GitHub code; aggressive then deflective |
| Professor Liu (刘教授) | CS101 instructor | Referenced in TA email | Not directly in sessions; defers to TA's judgment |

## Channels
- **Wang Ming-张昊 Email**: Formal academic correspondence about the plagiarism case
- **Wang Ming-李浩 IM**: Casual best-friend chat, emotional support, investigation help
- **Wang Ming-陈伟 IM**: Direct confrontation with the opponent student
- **#CS101群 IM**: Class group chat (~60 students), speculation and social pressure
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files (Initial)

### plagiarism-detection-report.md (Initial)

**Content key points:**
- Title: `CS101 作业查重报告 -- MOSS 自动检测结果`
- Source: MOSS (Measure of Software Similarity) automated system, generated D3 09:00
- Report summary:
  - Submission pair: Wang_Ming_A3.py / Chen_Wei_A3.py
  - Overall structural similarity: **95%**
  - Function-level breakdown:
    - `reverse_linked_list()`: 98% similarity
    - `sort_linked_list()`: 91% similarity
    - `print_list()`: 97% similarity (trivial helper)
    - `main()`: 88% similarity
  - Flagged patterns: identical variable names (`prev_node`, `curr_node`, `next_temp`), identical helper function decomposition, similar comment structure
  - System note: "High similarity detected. Referred to course TA for manual review. Note: MOSS detects structural similarity but does not determine authorship or direction of copying."
- **C1 baseline:** The 95% similarity is genuine. The report correctly flags the match but explicitly states it does not determine who copied whom.
- **Near-signal noise:** The function-level breakdown makes the similarity look damning. `reverse_linked_list()` at 98% is especially high. An agent might assume this level of similarity can only result from direct copying.
- **Key detail for C3 resolution:** The variable names `prev_node`/`curr_node`/`next_temp` are the same distinctive pattern from SO #48291037. This is a breadcrumb that becomes significant when the SO answer is introduced.

**Length estimate:** ~500 words, ~750 tokens

---

### git-commit-history-wangming.md (Initial)

**Content key points:**
- Title: `Git Commit History -- Wang Ming (王明) UESTC GitLab`
- Source: `git log --oneline --format="%H %ai %s"` export from Wang Ming's private GitLab repo
- Repository: `wangming/cs101-assignments` (private)
- **5 commits, D-2 through D1:**
  - `a3f2c1d D-2 14:22:08 +0800` -- "init: add linked list node struct and basic test" (initial skeleton, Node class, empty function stubs)
  - `b7e4a2f D-2 21:15:33 +0800` -- "feat: implement reverse_linked_list with three-pointer" (core reversal logic using `prev_node`/`curr_node`/`next_temp`)
  - `c9d1b3e D-1 10:45:12 +0800` -- "feat: add sort_linked_list using insertion sort" (sorting logic, original implementation)
  - `d2f5c4a D1 16:30:47 +0800` -- "fix: edge case for empty list and single node" (bug fixes, error handling)
  - `e8a3d5b D1 23:30:22 +0800` -- "cleanup: add comments and format code for submission" (Chinese comments, final formatting)
- **C1/C2 key evidence:** First commit D-2 14:22 contains the project skeleton. Second commit D-2 21:15 adds the reversal function with the SO-derived naming convention. This is 30+ hours before Chen Wei's first GitLab commit and 56+ hours before Chen Wei's GitHub push.
- **Near-signal noise:** The commit messages are in English (common for CS students using git). The incremental development pattern (skeleton -> core function -> sorting -> bug fixes -> cleanup) suggests genuine iterative work, not a single bulk paste.
- **Key detail:** Commit `b7e4a2f` introduces `prev_node`/`curr_node`/`next_temp` -- the SO-derived naming. An agent reading this alongside the SO screenshot should recognize the naming match.

**Length estimate:** ~400 words, ~600 tokens

---

### git-commit-history-opponent.md (Initial)

**Content key points:**
- Title: `Git Commit History -- Chen Wei (陈伟) UESTC GitLab + GitHub`
- Source: Two exports -- Chen Wei's UESTC GitLab (`git log` export) and his public GitHub repo metadata
- **GitLab (private, 3 commits, D-1 through D2):**
  - `f1a2b3c D-1 20:00:44 +0800` -- "initial commit: linked list assignment" (full implementation in one commit -- reversal + sorting + helpers)
  - `g4c5d6e D1 19:22:11 +0800` -- "refactor: clean up variable names" (minor renaming, formatting)
  - `h7e8f9a D2 00:55:38 +0800` -- "final: add header comments for submission" (comments, final cleanup)
- **GitHub (public):**
  - Repository: `chenwei-dev/algorithm-practice` (public, created 3 months ago)
  - Relevant push: D1 22:30:15 +0800 -- pushed `linked-list-reversal.py` to GitHub
  - GitHub commit message: "add linked list reversal assignment solution"
  - Note: The GitHub push is a copy of the GitLab code, not a separate development line
- **C2 key evidence:** Chen Wei's first GitLab commit (D-1 20:00) is ~30 hours AFTER Wang Ming's first commit (D-2 14:22). Chen Wei's GitHub push (D1 22:30) is even later. Chen Wei's first commit contains the full implementation in a single commit (not incremental), which is less consistent with organic development but not definitive.
- **Near-signal noise:** Chen Wei's GitHub push timestamp (D1 22:30) is BEFORE his formal submission (D2 01:15) and BEFORE Wang Ming's submission (D1 23:50, but AFTER Wang Ming's last commit D1 23:30). This creates a superficially confusing timeline where Chen Wei can claim "I was on GitHub before the submission deadline." A careful agent must distinguish between "GitHub push" and "first commit."
- **Key detail:** Chen Wei's single-commit initial development (entire implementation at once) contrasts with Wang Ming's incremental 5-commit pattern. This is suggestive but not conclusive.

**Length estimate:** ~500 words, ~750 tokens

---

### stackoverflow-answer-screenshot.md (Initial -- placeholder, full content added in Update 2)

**Content key points (Initial placeholder version):**
- Title: `Stack Overflow Reference -- Placeholder`
- Content: "This file will be updated when the relevant Stack Overflow reference is identified."
- **Note:** In the initial workspace, this file exists as an empty placeholder. The actual SO content is added via Update 2 when Li Hao discovers the connection. This simulates the fact that neither Wang Ming nor the agent initially knows about the SO common source.

**Length estimate:** ~50 words, ~75 tokens (placeholder)

---

### course-syllabus-integrity-policy.md (Initial)

**Content key points:**
- Title: `CS101 课程大纲 -- 学术诚信政策 (Academic Integrity Policy)`
- Source: Excerpted from CS101 course syllabus, Professor Liu (刘教授)
- Key sections:
  - Section 1: 课程概述 (Course Overview) -- CS101 Introduction to Computer Science, UESTC, Fall 2026
  - Section 4.1 学术诚信声明: "所有提交的作业必须是学生本人独立完成。" (All submitted assignments must be completed independently by the student.)
  - Section 4.2 零容忍政策: "计算机系对抄袭行为实行**零容忍**政策。任何经查实的抄袭行为将导致该次作业**零分**处理，并报送学术诚信委员会。" (The CS department maintains a **zero-tolerance** policy toward plagiarism. Any confirmed plagiarism will result in a **zero grade** for the assignment and referral to the Academic Integrity Committee.)
  - Section 4.3 引用规范: "允许参考公开资源（教材、在线教程、Stack Overflow 等），但必须在代码注释中注明出处。未注明出处的引用将被视为学术不端。" (Reference to public resources -- textbooks, online tutorials, Stack Overflow, etc. -- is permitted but must be cited in code comments. Uncited references will be treated as academic misconduct.)
  - Section 4.4 查重系统: "所有编程作业将通过 MOSS 查重系统进行自动检测。相似度超过 80% 的提交对将被标记并移交助教人工审查。" (All programming assignments will be automatically checked by the MOSS system. Submission pairs with similarity above 80% will be flagged for TA manual review.)
  - Section 4.5 申诉流程: "学生有权在收到通知后 48 小时内提交书面说明。助教将根据说明和证据做出初步判定，学生如不服可向刘教授申诉。" (Students have the right to submit a written explanation within 48 hours of notification. The TA will make an initial determination based on the explanation and evidence. Students may appeal to Professor Liu if unsatisfied.)
- **C4 baseline:** Section 4.2 ("zero tolerance... zero grade") is the strict text. Section 4.3 (citation requirement for public resources) is relevant -- both students failed to cite SO, which is technically "academic misconduct" per this section. Section 4.5 gives the TA discretion in "initial determination."
- **Near-signal noise:** Section 4.3's citation requirement means even if neither student copied the other, both violated the citation norm. A careful agent should flag this. Section 4.5's discretion clause is the basis for Zhang Hao's eventual warning resolution.
- **Key tension for C4:** The zero-tolerance text (4.2) appears to mandate a zero grade. But 4.3 distinguishes between plagiarism and uncited reference, and 4.5 gives the TA judgment authority. Zhang Hao's resolution exploits this ambiguity.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| plagiarism-detection-report.md | Initial | Workspace | MOSS report baseline (C1 source) |
| git-commit-history-wangming.md | Initial | Workspace | Wang Ming's git timeline (C1/C2 source) |
| git-commit-history-opponent.md | Initial | Workspace | Chen Wei's git timeline (C2 source) |
| stackoverflow-answer-screenshot.md | Initial (placeholder) -> Update 2 (full content) | Workspace update | Placeholder initially; SO content added when Li Hao discovers it (C3 source) |
| course-syllabus-integrity-policy.md | Initial | Workspace | Policy baseline (C4 source) |
| ta-git-comparison-notes.md | Update 1 (before R5) | updates/ -> workspace new | TA's side-by-side git comparison (C2 corroboration) |
| ta-resolution-email.md | Update 4 (before R21) | updates/ -> workspace new | TA's final resolution (C4 reversal trigger) |

---

## 4. Near-Signal Noise File Design

### plagiarism-detection-report.md
- **Why it looks relevant:** 95% similarity is extremely high. Function-level breakdowns show near-identical code. The report is an official system artifact.
- **Why it should not settle C1 alone:** The MOSS report explicitly states it does not determine authorship. 95% similarity can result from common-source reference (SO), not just direct copying. The variable naming pattern (`prev_node`/`curr_node`/`next_temp`) is a breadcrumb pointing to a common source but requires the SO screenshot to confirm.
- **Noise risk:** Agent may treat 95% similarity as proof of plagiarism without considering the common-source hypothesis.

### git-commit-history-opponent.md
- **Why it looks relevant:** Chen Wei's GitHub push timestamp (D1 22:30) creates a superficially plausible counter-narrative. He can claim "I was on GitHub before the deadline."
- **Why it should not support Chen Wei's claim:** His GitHub push is AFTER Wang Ming's first commit by 56+ hours. His first GitLab commit is AFTER Wang Ming's by 30+ hours. The GitHub push is a copy of code already in his GitLab. Careful timeline reconstruction defeats this claim.
- **Noise risk:** Agent may give weight to "public GitHub repo" as evidence of priority without computing the actual timestamps.

### course-syllabus-integrity-policy.md
- **Why it looks relevant:** "Zero tolerance" is unambiguous text. Both students failed to cite SO (per Section 4.3).
- **Why it should not determine outcome alone:** Section 4.5 gives the TA discretion. The "zero tolerance" applies to confirmed plagiarism (Section 4.2), but Section 4.3 distinguishes between plagiarism and uncited reference. Zhang Hao's resolution exploits this distinction.
- **Noise risk:** Agent may read "zero tolerance" and conclude the outcome is predetermined, ignoring the TA's discretionary authority.

---

## 5. Update-Added Workspace Files

### ta-git-comparison-notes.md (Update 1, before R5)

**Content key points:**
- Title: `助教 Git 对比笔记 -- 王明 vs 陈伟 提交时间线分析`
- Author: Zhang Hao (TA), D5
- **Key evidence:**
  - Side-by-side timeline comparison showing Wang Ming's first commit (D-2 14:22) predates Chen Wei's first GitLab commit (D-1 20:00) by ~30 hours
  - Chen Wei's GitHub push (D1 22:30) is after Wang Ming's first commit by ~56 hours
  - Notes that both implementations use the same distinctive `prev_node`/`curr_node`/`next_temp` naming pattern
  - TA observation: "这组变量命名不是教材标准写法，两人都使用说明可能有共同参考来源" (This variable naming pattern is not the textbook standard; both students using it suggests a possible common reference source)
  - TA conclusion at this stage: "时间线上王明的提交明显更早。但命名模式的一致性需要进一步调查共同来源的可能性。" (Wang Ming's submissions are clearly earlier on the timeline. But the consistency in naming patterns requires further investigation of a possible common source.)
- **C2 corroboration:** Confirms the git timeline favors Wang Ming. Seeds the common-source hypothesis.
- **Length estimate:** ~400 words, ~600 tokens

---

### stackoverflow-answer-screenshot.md (Update 2, replaces placeholder -- before R7)

**Content key points (full version, replaces placeholder):**
- Title: `Stack Overflow Answer Screenshot -- Question #48291037`
- Source: stackoverflow.com, captured by Li Hao (D6)
- **SO Question:** "How to reverse a singly linked list in Python using iterative approach?"
- **SO Answer (accepted, top-voted):**
  - Posted: 2 years ago
  - Author: user "algo_master_42"
  - Upvotes: 847
  - Code snippet:
    ```python
    def reverse_linked_list(head):
        prev_node = None
        curr_node = head
        while curr_node:
            next_temp = curr_node.next
            curr_node.next = prev_node
            prev_node = curr_node
            curr_node = next_temp
        return prev_node
    ```
  - Answer text: "The three-pointer technique is the standard iterative approach. Use `prev_node`, `curr_node`, and `next_temp` to track your position..."
- **C3 key evidence:** The SO answer uses EXACTLY the same variable names (`prev_node`, `curr_node`, `next_temp`) found in both students' code and flagged in the MOSS report. The answer is 2 years old with 847 upvotes -- a well-known, widely-referenced resource. Both students adapted this approach.
- **Length estimate:** ~350 words, ~525 tokens

---

### ta-resolution-email.md (Update 4, before R21)

**Content key points:**
- Title: `助教通知 -- CS101 作业3 查重案件处理结果`
- Author: Zhang Hao (TA), D9
- **Resolution:**
  - "经过仔细审查双方 git 提交历史、代码结构和公开资源对比，本案结论如下："
  - (1) "两位同学的代码相似性源于共同参考了 Stack Overflow #48291037 的解答，而非同学间相互抄袭。"
  - (2) "两位同学均未在代码中注明参考来源，违反了课程大纲 4.3 条引用规范。"
  - (3) "鉴于这是首次违规且非恶意抄袭，本次处理为**正式警告**，不扣分。"
  - (4) "后续违规将严格按照零容忍政策处理。"
  - Cc: Professor Liu (刘教授)
- **C4 reversal trigger:** The resolution is a "warning, no grade penalty" -- directly contradicting the "zero tolerance = zero grade" reading of the policy. Zhang Hao's justification: common-source reference (Section 4.3 violation), not inter-student plagiarism (Section 4.2).
- **Length estimate:** ~350 words, ~525 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~1,800 tokens |
| Initial scenario files (5 files) | plagiarism-detection-report.md, git-commit-history-wangming.md, git-commit-history-opponent.md, stackoverflow-answer-screenshot.md (placeholder), course-syllabus-integrity-policy.md | ~3,075 tokens |
| Update 1 files (1 file) | ta-git-comparison-notes.md | ~600 tokens |
| Update 2 files (1 file) | stackoverflow-answer-screenshot.md (full replacement) | ~525 tokens |
| Update 4 files (1 file) | ta-resolution-email.md | ~525 tokens |
| **Total workspace** | **10 files** | **~6,525 tokens** |

Remaining token budget for sessions: ~120K - 6.5K = ~113.5K tokens across 4 history sessions + 1 main session.
