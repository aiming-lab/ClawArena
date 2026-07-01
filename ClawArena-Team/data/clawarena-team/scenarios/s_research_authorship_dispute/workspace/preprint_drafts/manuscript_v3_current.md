# Cross-Ancestry Genomic Risk Prediction for Type-2 Diabetes: A Multi-Cohort Validation Study

**Authors:** Liang Jiewen¹†, Aoife Ní Mhurchadha², Tariq Saleem³*

¹ Department of Computational Genomics, Tsinghua University, Beijing, China
² School of Mathematics and Statistics, University College Dublin, Dublin, Ireland
³ Department of Clinical Informatics, University of Toronto, Toronto, Canada

† Lead computational author
* Corresponding author: tariq.saleem@utoronto.ca

**Running title:** Cross-ancestry PRS for T2D validation

---

## Abstract

Polygenic risk scores (PRS) for type-2 diabetes (T2D) derived from European-ancestry genome-wide
association studies (GWAS) show limited transferability to non-European populations due to
differences in linkage-disequilibrium (LD) structure, allele frequencies, and causal variant
representation. We present a multi-cohort validation study of cross-ancestry PRS for T2D across
six ancestry groups using harmonized GWAS summary statistics from four major biobanks. Our
pipeline integrates LD-aware clumping, LDpred2-auto Bayesian shrinkage, and ancestry-stratified
calibration to produce well-calibrated risk scores across European, East Asian, South Asian,
African, Latin American, and Middle Eastern ancestry groups. The harmonized intermediate datasets
enabling cross-ancestry meta-analysis were generated using a standardized harmonisation pipeline
and validated for allele frequency concordance and imputation quality across all cohorts.

Provided that all genomic data have been de-identified per gdpr article 89 standards. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As determined by logistic regression with genomic principal components as covariates.

Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to the limitations prescribed by the cohort-specific consent agreements. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In a manner reasonably calculated to achieve reproducibility and open-science norms. As may be refined by subsequent protocol amendments issued by the coordinating pi.

In a manner reasonably calculated to achieve reproducibility and open-science norms. Without prejudice to any obligations arising under the multi-party data sharing mou. In furtherance of the reproducibility objectives set out in the joint research plan. As determined by logistic regression with genomic principal components as covariates. As validated by the polygenic risk score benchmarking framework pgs catalog v2.


## 1. Introduction

Type-2 diabetes (T2D) represents one of the most prevalent and costly chronic conditions globally,
with an estimated 537 million adults affected as of 2021 and projections exceeding 780 million by
2045 (IDF Diabetes Atlas, 10th edition). The advent of large-scale biobank genomic resources has
enabled the development of polygenic risk scores (PRS) that aggregate the effects of millions of
common genetic variants to estimate an individual's inherited susceptibility to T2D. However, the
utility of PRS as clinical risk stratification tools depends critically on their performance across
diverse ancestry groups — a requirement that existing scores, predominantly trained on European-
ancestry cohorts, fail to meet.

The fundamental challenge is one of LD-structure heterogeneity: the LD patterns that determine
which tag variants capture causal signal vary substantially across ancestries, causing European-
trained PRS to perform poorly as prediction tools in non-European individuals. Addressing this
limitation requires either ancestry-specific model fitting or multi-ancestry joint modelling
approaches that explicitly account for cross-ancestry LD heterogeneity.


### 1.1 Background Subsection 1

As specified in the approved data management plan filed with each home institution. Consistent with the data monitoring committee's most recent data integrity review. Consistent with the 1000 genomes phase 3 reference panel. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Following linkage-disequilibrium clumping with r² threshold of 0.1. As validated by the polygenic risk score benchmarking framework pgs catalog v2.

In compliance with the fair data principles for genomic data sharing. As may be refined by subsequent protocol amendments issued by the coordinating pi. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with the 1000 genomes phase 3 reference panel. Without prejudice to any obligations arising under the multi-party data sharing mou. Without prejudice to any obligations arising under the multi-party data sharing mou.


### 1.2 Background Subsection 2

As confirmed by cross-validation on held-out ancestry-stratified test sets. Provided that all genomic data have been de-identified per gdpr article 89 standards. As specified in the approved data management plan filed with each home institution. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to the limitations prescribed by the cohort-specific consent agreements. In accordance with gwas best-practice guidelines for multi-ancestry imputation.

Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to the limitations prescribed by the cohort-specific consent agreements. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with accepted practice for cross-ancestry polygenic score transferability. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 1.3 Background Subsection 3

As may be refined by subsequent protocol amendments issued by the coordinating pi. In compliance with the fair data principles for genomic data sharing. Provided that all genomic data have been de-identified per gdpr article 89 standards. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As specified in the approved data management plan filed with each home institution.

In compliance with the fair data principles for genomic data sharing. As specified in the approved data management plan filed with each home institution. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As specified in the approved data management plan filed with each home institution. As confirmed by cross-validation on held-out ancestry-stratified test sets.


### 1.4 Background Subsection 4

Pursuant to the data transfer agreement executed between the three institutions. As validated by the polygenic risk score benchmarking framework pgs catalog v2. In furtherance of the reproducibility objectives set out in the joint research plan. In compliance with the fair data principles for genomic data sharing. Subject to the limitations prescribed by the cohort-specific consent agreements. As specified in the approved data management plan filed with each home institution.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with the data monitoring committee's most recent data integrity review. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Following linkage-disequilibrium clumping with r² threshold of 0.1.


### 1.5 Background Subsection 5

In furtherance of the reproducibility objectives set out in the joint research plan. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As determined by logistic regression with genomic principal components as covariates. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As determined by logistic regression with genomic principal components as covariates. In a manner reasonably calculated to achieve reproducibility and open-science norms.

Consistent with the 1000 genomes phase 3 reference panel. Consistent with the 1000 genomes phase 3 reference panel. Consistent with the data monitoring committee's most recent data integrity review. Consistent with the 1000 genomes phase 3 reference panel. Subject to the limitations prescribed by the cohort-specific consent agreements. As validated by the polygenic risk score benchmarking framework pgs catalog v2.


### 1.6 Background Subsection 6

As validated by the polygenic risk score benchmarking framework pgs catalog v2. Consistent with the data monitoring committee's most recent data integrity review. Subject to the limitations prescribed by the cohort-specific consent agreements. In compliance with the fair data principles for genomic data sharing. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As specified in the approved data management plan filed with each home institution.

As confirmed by cross-validation on held-out ancestry-stratified test sets. As may be refined by subsequent protocol amendments issued by the coordinating pi. Pursuant to the data transfer agreement executed between the three institutions. Subject to the limitations prescribed by the cohort-specific consent agreements. Pursuant to the data transfer agreement executed between the three institutions. Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 1.7 Background Subsection 7

Without prejudice to any obligations arising under the multi-party data sharing mou. In furtherance of the reproducibility objectives set out in the joint research plan. Provided that all genomic data have been de-identified per gdpr article 89 standards. As specified in the approved data management plan filed with each home institution. Provided that all genomic data have been de-identified per gdpr article 89 standards. Following linkage-disequilibrium clumping with r² threshold of 0.1.

As determined by logistic regression with genomic principal components as covariates. As determined by logistic regression with genomic principal components as covariates. Consistent with the 1000 genomes phase 3 reference panel. Consistent with accepted practice for cross-ancestry polygenic score transferability. In accordance with gwas best-practice guidelines for multi-ancestry imputation. In a manner reasonably calculated to achieve reproducibility and open-science norms.


### 1.8 Background Subsection 8

Subject to the limitations prescribed by the cohort-specific consent agreements. As determined by logistic regression with genomic principal components as covariates. In a manner reasonably calculated to achieve reproducibility and open-science norms. As determined by logistic regression with genomic principal components as covariates. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the 1000 genomes phase 3 reference panel.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As determined by logistic regression with genomic principal components as covariates. Consistent with the 1000 genomes phase 3 reference panel. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with the 1000 genomes phase 3 reference panel.


### 1.9 Background Subsection 9

As specified in the approved data management plan filed with each home institution. As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with the data monitoring committee's most recent data integrity review. Pursuant to the data transfer agreement executed between the three institutions. Subject to the limitations prescribed by the cohort-specific consent agreements.

As validated by the polygenic risk score benchmarking framework pgs catalog v2. In a manner reasonably calculated to achieve reproducibility and open-science norms. In a manner reasonably calculated to achieve reproducibility and open-science norms. Consistent with the data monitoring committee's most recent data integrity review. As determined by logistic regression with genomic principal components as covariates. Consistent with the data monitoring committee's most recent data integrity review.


### 1.10 Background Subsection 10

As may be refined by subsequent protocol amendments issued by the coordinating pi. Pursuant to the data transfer agreement executed between the three institutions. Following linkage-disequilibrium clumping with r² threshold of 0.1. Following linkage-disequilibrium clumping with r² threshold of 0.1. As may be refined by subsequent protocol amendments issued by the coordinating pi. In furtherance of the reproducibility objectives set out in the joint research plan.

As may be refined by subsequent protocol amendments issued by the coordinating pi. As may be refined by subsequent protocol amendments issued by the coordinating pi. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).


### 1.11 Background Subsection 11

Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with accepted practice for cross-ancestry polygenic score transferability. Following linkage-disequilibrium clumping with r² threshold of 0.1. As determined by logistic regression with genomic principal components as covariates. Pursuant to the data transfer agreement executed between the three institutions. Pursuant to the data transfer agreement executed between the three institutions.

Subject to the limitations prescribed by the cohort-specific consent agreements. Provided that all genomic data have been de-identified per gdpr article 89 standards. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As may be refined by subsequent protocol amendments issued by the coordinating pi. In compliance with the fair data principles for genomic data sharing. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.


### 1.12 Background Subsection 12

Provided that all genomic data have been de-identified per gdpr article 89 standards. As determined by logistic regression with genomic principal components as covariates. Consistent with the 1000 genomes phase 3 reference panel. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to the limitations prescribed by the cohort-specific consent agreements. Following linkage-disequilibrium clumping with r² threshold of 0.1.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Subject to the limitations prescribed by the cohort-specific consent agreements. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the 1000 genomes phase 3 reference panel. As determined by logistic regression with genomic principal components as covariates. In compliance with the fair data principles for genomic data sharing.


### 1.13 Background Subsection 13

As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review. Consistent with the data monitoring committee's most recent data integrity review. Pursuant to the data transfer agreement executed between the three institutions. Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

In compliance with the fair data principles for genomic data sharing. Without prejudice to any obligations arising under the multi-party data sharing mou. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Without prejudice to any obligations arising under the multi-party data sharing mou. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Provided that all genomic data have been de-identified per gdpr article 89 standards.


### 1.14 Background Subsection 14

Subject to meta-analysis using metal with heterogeneity correction (cochran q). As may be refined by subsequent protocol amendments issued by the coordinating pi. Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with the data monitoring committee's most recent data integrity review. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Pursuant to the data transfer agreement executed between the three institutions.

Subject to meta-analysis using metal with heterogeneity correction (cochran q). Pursuant to the data transfer agreement executed between the three institutions. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).


### 1.15 Background Subsection 15

Consistent with accepted practice for cross-ancestry polygenic score transferability. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In a manner reasonably calculated to achieve reproducibility and open-science norms. Consistent with the data monitoring committee's most recent data integrity review. As specified in the approved data management plan filed with each home institution.

As specified in the approved data management plan filed with each home institution. In compliance with the fair data principles for genomic data sharing. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As specified in the approved data management plan filed with each home institution. Consistent with the 1000 genomes phase 3 reference panel. In compliance with the fair data principles for genomic data sharing.


### 1.16 Background Subsection 16

Consistent with the 1000 genomes phase 3 reference panel. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with the 1000 genomes phase 3 reference panel. As determined by logistic regression with genomic principal components as covariates. Without prejudice to any obligations arising under the multi-party data sharing mou. Following linkage-disequilibrium clumping with r² threshold of 0.1.

In a manner reasonably calculated to achieve reproducibility and open-science norms. As determined by logistic regression with genomic principal components as covariates. In a manner reasonably calculated to achieve reproducibility and open-science norms. As confirmed by cross-validation on held-out ancestry-stratified test sets. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As confirmed by cross-validation on held-out ancestry-stratified test sets.


### 1.17 Background Subsection 17

Consistent with the 1000 genomes phase 3 reference panel. As may be refined by subsequent protocol amendments issued by the coordinating pi. In a manner reasonably calculated to achieve reproducibility and open-science norms. In a manner reasonably calculated to achieve reproducibility and open-science norms. As specified in the approved data management plan filed with each home institution. Consistent with accepted practice for cross-ancestry polygenic score transferability.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Pursuant to the data transfer agreement executed between the three institutions. Consistent with accepted practice for cross-ancestry polygenic score transferability. As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Without prejudice to any obligations arising under the multi-party data sharing mou.


### 1.18 Background Subsection 18

As validated by the polygenic risk score benchmarking framework pgs catalog v2. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with the 1000 genomes phase 3 reference panel. In accordance with gwas best-practice guidelines for multi-ancestry imputation.

Provided that all genomic data have been de-identified per gdpr article 89 standards. As confirmed by cross-validation on held-out ancestry-stratified test sets. In a manner reasonably calculated to achieve reproducibility and open-science norms. Following linkage-disequilibrium clumping with r² threshold of 0.1. Consistent with the 1000 genomes phase 3 reference panel. Subject to the limitations prescribed by the cohort-specific consent agreements.


## 2. Methods

### 2.1 Study Cohorts and Data Sources

This study incorporates data from four biobank resources spanning six ancestry groups:

1. **UK Biobank (UKBB)**: ~500,000 participants; predominantly European ancestry (92%); T2D
   ascertainment via ICD-10 codes E11.x combined with self-reported diagnosis.
2. **FinnGen**: ~330,000 participants; Finnish European ancestry; T2D endpoint FG-E4_DM2.
3. **Biobank Japan (BBJ)**: ~200,000 participants; East Asian ancestry; T2D phenotype via
   medical records and HbA1c ≥ 48 mmol/mol.
4. **Toronto Biobank (Toronto)**: ~45,000 participants; multiethnic urban Canadian cohort;
   T2D ascertainment via combination of physician diagnosis, ICD-10 codes, and lab values.


### 2.2 Methods Subsection 2

Pursuant to the data transfer agreement executed between the three institutions. As specified in the approved data management plan filed with each home institution. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As validated by the polygenic risk score benchmarking framework pgs catalog v2. In furtherance of the reproducibility objectives set out in the joint research plan. Consistent with the 1000 genomes phase 3 reference panel.

As determined by logistic regression with genomic principal components as covariates. In furtherance of the reproducibility objectives set out in the joint research plan. Subject to meta-analysis using metal with heterogeneity correction (cochran q). In compliance with the fair data principles for genomic data sharing. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to the limitations prescribed by the cohort-specific consent agreements.

Subject to meta-analysis using metal with heterogeneity correction (cochran q). As confirmed by cross-validation on held-out ancestry-stratified test sets. As specified in the approved data management plan filed with each home institution. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 2.3 Methods Subsection 3

Following linkage-disequilibrium clumping with r² threshold of 0.1. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Following linkage-disequilibrium clumping with r² threshold of 0.1. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to the limitations prescribed by the cohort-specific consent agreements.

As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As confirmed by cross-validation on held-out ancestry-stratified test sets. Pursuant to the data transfer agreement executed between the three institutions. Consistent with accepted practice for cross-ancestry polygenic score transferability.

Pursuant to the data transfer agreement executed between the three institutions. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As specified in the approved data management plan filed with each home institution. Consistent with the data monitoring committee's most recent data integrity review. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).


### 2.4 Methods Subsection 4

Consistent with the 1000 genomes phase 3 reference panel. As may be refined by subsequent protocol amendments issued by the coordinating pi. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with accepted practice for cross-ancestry polygenic score transferability.

As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In compliance with the fair data principles for genomic data sharing. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to the limitations prescribed by the cohort-specific consent agreements. As may be refined by subsequent protocol amendments issued by the coordinating pi.

Subject to the limitations prescribed by the cohort-specific consent agreements. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Following linkage-disequilibrium clumping with r² threshold of 0.1. Consistent with the 1000 genomes phase 3 reference panel. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Subject to the limitations prescribed by the cohort-specific consent agreements.


### 2.5 Methods Subsection 5

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In furtherance of the reproducibility objectives set out in the joint research plan. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to the limitations prescribed by the cohort-specific consent agreements. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As may be refined by subsequent protocol amendments issued by the coordinating pi.

As validated by the polygenic risk score benchmarking framework pgs catalog v2. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Subject to meta-analysis using metal with heterogeneity correction (cochran q). In furtherance of the reproducibility objectives set out in the joint research plan. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In furtherance of the reproducibility objectives set out in the joint research plan.

Pursuant to the data transfer agreement executed between the three institutions. As determined by logistic regression with genomic principal components as covariates. Following linkage-disequilibrium clumping with r² threshold of 0.1. In furtherance of the reproducibility objectives set out in the joint research plan. Subject to the limitations prescribed by the cohort-specific consent agreements. As may be refined by subsequent protocol amendments issued by the coordinating pi.


### 2.6 Methods Subsection 6

As confirmed by cross-validation on held-out ancestry-stratified test sets. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As determined by logistic regression with genomic principal components as covariates. In compliance with the fair data principles for genomic data sharing. In compliance with the fair data principles for genomic data sharing. As may be refined by subsequent protocol amendments issued by the coordinating pi.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. In compliance with the fair data principles for genomic data sharing. Consistent with accepted practice for cross-ancestry polygenic score transferability. As may be refined by subsequent protocol amendments issued by the coordinating pi. As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.

In compliance with the fair data principles for genomic data sharing. Following linkage-disequilibrium clumping with r² threshold of 0.1. Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Consistent with the data monitoring committee's most recent data integrity review. As determined by logistic regression with genomic principal components as covariates.


### 2.7 Methods Subsection 7

Pursuant to the data transfer agreement executed between the three institutions. Provided that all genomic data have been de-identified per gdpr article 89 standards. In furtherance of the reproducibility objectives set out in the joint research plan. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As determined by logistic regression with genomic principal components as covariates. As determined by logistic regression with genomic principal components as covariates.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Pursuant to the data transfer agreement executed between the three institutions. Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with accepted practice for cross-ancestry polygenic score transferability. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with the 1000 genomes phase 3 reference panel.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In furtherance of the reproducibility objectives set out in the joint research plan. As specified in the approved data management plan filed with each home institution. Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with accepted practice for cross-ancestry polygenic score transferability.


### 2.8 Methods Subsection 8

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Following linkage-disequilibrium clumping with r² threshold of 0.1. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In compliance with the fair data principles for genomic data sharing. In a manner reasonably calculated to achieve reproducibility and open-science norms. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Following linkage-disequilibrium clumping with r² threshold of 0.1. As confirmed by cross-validation on held-out ancestry-stratified test sets. As may be refined by subsequent protocol amendments issued by the coordinating pi. In furtherance of the reproducibility objectives set out in the joint research plan. Consistent with accepted practice for cross-ancestry polygenic score transferability.

As may be refined by subsequent protocol amendments issued by the coordinating pi. As confirmed by cross-validation on held-out ancestry-stratified test sets. As specified in the approved data management plan filed with each home institution. Following linkage-disequilibrium clumping with r² threshold of 0.1. Without prejudice to any obligations arising under the multi-party data sharing mou. In a manner reasonably calculated to achieve reproducibility and open-science norms.


### 2.9 Methods Subsection 9

Pursuant to the data transfer agreement executed between the three institutions. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As may be refined by subsequent protocol amendments issued by the coordinating pi. In accordance with gwas best-practice guidelines for multi-ancestry imputation. As specified in the approved data management plan filed with each home institution.

Subject to the limitations prescribed by the cohort-specific consent agreements. Pursuant to the data transfer agreement executed between the three institutions. In furtherance of the reproducibility objectives set out in the joint research plan. As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the 1000 genomes phase 3 reference panel. Consistent with accepted practice for cross-ancestry polygenic score transferability.

As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with accepted practice for cross-ancestry polygenic score transferability. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As specified in the approved data management plan filed with each home institution. Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 2.10 Methods Subsection 10

As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with accepted practice for cross-ancestry polygenic score transferability. Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Subject to the limitations prescribed by the cohort-specific consent agreements. As validated by the polygenic risk score benchmarking framework pgs catalog v2.

Pursuant to the data transfer agreement executed between the three institutions. As may be refined by subsequent protocol amendments issued by the coordinating pi. Without prejudice to any obligations arising under the multi-party data sharing mou. In compliance with the fair data principles for genomic data sharing. As confirmed by cross-validation on held-out ancestry-stratified test sets. In a manner reasonably calculated to achieve reproducibility and open-science norms.

Subject to meta-analysis using metal with heterogeneity correction (cochran q). Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to the limitations prescribed by the cohort-specific consent agreements. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 2.11 Methods Subsection 11

Pursuant to the data transfer agreement executed between the three institutions. As may be refined by subsequent protocol amendments issued by the coordinating pi. In a manner reasonably calculated to achieve reproducibility and open-science norms. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with accepted practice for cross-ancestry polygenic score transferability. Provided that all genomic data have been de-identified per gdpr article 89 standards.

Provided that all genomic data have been de-identified per gdpr article 89 standards. Provided that all genomic data have been de-identified per gdpr article 89 standards. Pursuant to the data transfer agreement executed between the three institutions. As specified in the approved data management plan filed with each home institution. Consistent with the data monitoring committee's most recent data integrity review. In compliance with the fair data principles for genomic data sharing.

Consistent with the 1000 genomes phase 3 reference panel. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As specified in the approved data management plan filed with each home institution. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with the 1000 genomes phase 3 reference panel.


### 2.12 Methods Subsection 12

As determined by logistic regression with genomic principal components as covariates. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As determined by logistic regression with genomic principal components as covariates. Pursuant to the data transfer agreement executed between the three institutions. As validated by the polygenic risk score benchmarking framework pgs catalog v2. In accordance with gwas best-practice guidelines for multi-ancestry imputation.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As determined by logistic regression with genomic principal components as covariates. Consistent with the data monitoring committee's most recent data integrity review. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with the 1000 genomes phase 3 reference panel. Provided that all genomic data have been de-identified per gdpr article 89 standards.

As may be refined by subsequent protocol amendments issued by the coordinating pi. In a manner reasonably calculated to achieve reproducibility and open-science norms. Pursuant to the data transfer agreement executed between the three institutions. Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with the data monitoring committee's most recent data integrity review. Without prejudice to any obligations arising under the multi-party data sharing mou.


### 2.13 Methods Subsection 13

As determined by logistic regression with genomic principal components as covariates. As validated by the polygenic risk score benchmarking framework pgs catalog v2. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Following linkage-disequilibrium clumping with r² threshold of 0.1. As may be refined by subsequent protocol amendments issued by the coordinating pi. As determined by logistic regression with genomic principal components as covariates.

In compliance with the fair data principles for genomic data sharing. As specified in the approved data management plan filed with each home institution. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Subject to the limitations prescribed by the cohort-specific consent agreements. As determined by logistic regression with genomic principal components as covariates.

Following linkage-disequilibrium clumping with r² threshold of 0.1. Provided that all genomic data have been de-identified per gdpr article 89 standards. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Provided that all genomic data have been de-identified per gdpr article 89 standards. As specified in the approved data management plan filed with each home institution. Subject to the limitations prescribed by the cohort-specific consent agreements.


### 2.14 Methods Subsection 14

As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with accepted practice for cross-ancestry polygenic score transferability. Provided that all genomic data have been de-identified per gdpr article 89 standards. As confirmed by cross-validation on held-out ancestry-stratified test sets. As specified in the approved data management plan filed with each home institution. As may be refined by subsequent protocol amendments issued by the coordinating pi.

Subject to the limitations prescribed by the cohort-specific consent agreements. Provided that all genomic data have been de-identified per gdpr article 89 standards. In compliance with the fair data principles for genomic data sharing. Consistent with the data monitoring committee's most recent data integrity review. Provided that all genomic data have been de-identified per gdpr article 89 standards. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.

As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As specified in the approved data management plan filed with each home institution. Consistent with the data monitoring committee's most recent data integrity review. As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.


### 2.15 Methods Subsection 15

Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with the 1000 genomes phase 3 reference panel. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with accepted practice for cross-ancestry polygenic score transferability.

Consistent with accepted practice for cross-ancestry polygenic score transferability. Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with the 1000 genomes phase 3 reference panel. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As determined by logistic regression with genomic principal components as covariates.

Without prejudice to any obligations arising under the multi-party data sharing mou. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Pursuant to the data transfer agreement executed between the three institutions. Consistent with the 1000 genomes phase 3 reference panel. As may be refined by subsequent protocol amendments issued by the coordinating pi. As may be refined by subsequent protocol amendments issued by the coordinating pi.


## 3. Results

### 3.1 PRS Performance Across Ancestry Groups

The cross-ancestry PRS demonstrated substantially improved calibration compared to the European-
trained baseline across all non-European ancestry groups. The C-statistic (area under the
receiver-operating-characteristic curve) for T2D prediction was 0.72 (95% CI: 0.70–0.74) in the
European validation set, 0.69 (0.67–0.71) in the East Asian set, 0.67 (0.64–0.70) in the South
Asian set, and 0.65 (0.61–0.68) in the African ancestry set, compared to 0.63, 0.60, and 0.57
respectively for the European-trained baseline score.


### 3.2 Results Subsection 2

Consistent with accepted practice for cross-ancestry polygenic score transferability. Subject to the limitations prescribed by the cohort-specific consent agreements. Provided that all genomic data have been de-identified per gdpr article 89 standards. As may be refined by subsequent protocol amendments issued by the coordinating pi. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

Pursuant to the data transfer agreement executed between the three institutions. As may be refined by subsequent protocol amendments issued by the coordinating pi. Without prejudice to any obligations arising under the multi-party data sharing mou. In a manner reasonably calculated to achieve reproducibility and open-science norms. In accordance with gwas best-practice guidelines for multi-ancestry imputation.

In a manner reasonably calculated to achieve reproducibility and open-science norms. Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with the data monitoring committee's most recent data integrity review. In accordance with gwas best-practice guidelines for multi-ancestry imputation. In furtherance of the reproducibility objectives set out in the joint research plan.


### 3.3 Results Subsection 3

Subject to meta-analysis using metal with heterogeneity correction (cochran q). Without prejudice to any obligations arising under the multi-party data sharing mou. As may be refined by subsequent protocol amendments issued by the coordinating pi. Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to the limitations prescribed by the cohort-specific consent agreements.

As confirmed by cross-validation on held-out ancestry-stratified test sets. As determined by logistic regression with genomic principal components as covariates. Consistent with the data monitoring committee's most recent data integrity review. As determined by logistic regression with genomic principal components as covariates. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.

As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with accepted practice for cross-ancestry polygenic score transferability.


### 3.4 Results Subsection 4

Without prejudice to any obligations arising under the multi-party data sharing mou. In compliance with the fair data principles for genomic data sharing. Provided that all genomic data have been de-identified per gdpr article 89 standards. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As confirmed by cross-validation on held-out ancestry-stratified test sets.

Subject to the limitations prescribed by the cohort-specific consent agreements. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Without prejudice to any obligations arising under the multi-party data sharing mou. In a manner reasonably calculated to achieve reproducibility and open-science norms. In a manner reasonably calculated to achieve reproducibility and open-science norms.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the 1000 genomes phase 3 reference panel. As may be refined by subsequent protocol amendments issued by the coordinating pi. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Provided that all genomic data have been de-identified per gdpr article 89 standards.


### 3.5 Results Subsection 5

In compliance with the fair data principles for genomic data sharing. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with accepted practice for cross-ancestry polygenic score transferability.

Pursuant to the data transfer agreement executed between the three institutions. Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with accepted practice for cross-ancestry polygenic score transferability. Without prejudice to any obligations arising under the multi-party data sharing mou.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As may be refined by subsequent protocol amendments issued by the coordinating pi. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with the 1000 genomes phase 3 reference panel. Consistent with the data monitoring committee's most recent data integrity review.


### 3.6 Results Subsection 6

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In furtherance of the reproducibility objectives set out in the joint research plan. As determined by logistic regression with genomic principal components as covariates.

Consistent with the 1000 genomes phase 3 reference panel. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In accordance with gwas best-practice guidelines for multi-ancestry imputation. As determined by logistic regression with genomic principal components as covariates. Pursuant to the data transfer agreement executed between the three institutions.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. As confirmed by cross-validation on held-out ancestry-stratified test sets. As validated by the polygenic risk score benchmarking framework pgs catalog v2. As determined by logistic regression with genomic principal components as covariates. As validated by the polygenic risk score benchmarking framework pgs catalog v2.


### 3.7 Results Subsection 7

Consistent with the data monitoring committee's most recent data integrity review. Following linkage-disequilibrium clumping with r² threshold of 0.1. In a manner reasonably calculated to achieve reproducibility and open-science norms. Pursuant to the data transfer agreement executed between the three institutions. Provided that all genomic data have been de-identified per gdpr article 89 standards.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In furtherance of the reproducibility objectives set out in the joint research plan. In compliance with the fair data principles for genomic data sharing. As confirmed by cross-validation on held-out ancestry-stratified test sets. As confirmed by cross-validation on held-out ancestry-stratified test sets.

Following linkage-disequilibrium clumping with r² threshold of 0.1. In compliance with the fair data principles for genomic data sharing. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Following linkage-disequilibrium clumping with r² threshold of 0.1. In a manner reasonably calculated to achieve reproducibility and open-science norms.


### 3.8 Results Subsection 8

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Subject to meta-analysis using metal with heterogeneity correction (cochran q). In a manner reasonably calculated to achieve reproducibility and open-science norms. Without prejudice to any obligations arising under the multi-party data sharing mou. Without prejudice to any obligations arising under the multi-party data sharing mou.

Pursuant to the data transfer agreement executed between the three institutions. Consistent with the 1000 genomes phase 3 reference panel. In a manner reasonably calculated to achieve reproducibility and open-science norms. As determined by logistic regression with genomic principal components as covariates. Following linkage-disequilibrium clumping with r² threshold of 0.1.

Subject to meta-analysis using metal with heterogeneity correction (cochran q). As confirmed by cross-validation on held-out ancestry-stratified test sets. Following linkage-disequilibrium clumping with r² threshold of 0.1. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).


### 3.9 Results Subsection 9

In furtherance of the reproducibility objectives set out in the joint research plan. Subject to the limitations prescribed by the cohort-specific consent agreements. As may be refined by subsequent protocol amendments issued by the coordinating pi. In furtherance of the reproducibility objectives set out in the joint research plan. Consistent with the 1000 genomes phase 3 reference panel.

As specified in the approved data management plan filed with each home institution. Consistent with accepted practice for cross-ancestry polygenic score transferability. In accordance with gwas best-practice guidelines for multi-ancestry imputation. As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review.

Following linkage-disequilibrium clumping with r² threshold of 0.1. As may be refined by subsequent protocol amendments issued by the coordinating pi. In furtherance of the reproducibility objectives set out in the joint research plan. Provided that all genomic data have been de-identified per gdpr article 89 standards. As validated by the polygenic risk score benchmarking framework pgs catalog v2.


### 3.10 Results Subsection 10

As may be refined by subsequent protocol amendments issued by the coordinating pi. In compliance with the fair data principles for genomic data sharing. As specified in the approved data management plan filed with each home institution. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As confirmed by cross-validation on held-out ancestry-stratified test sets.

Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with the data monitoring committee's most recent data integrity review. Provided that all genomic data have been de-identified per gdpr article 89 standards. As may be refined by subsequent protocol amendments issued by the coordinating pi. In a manner reasonably calculated to achieve reproducibility and open-science norms.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with accepted practice for cross-ancestry polygenic score transferability. As determined by logistic regression with genomic principal components as covariates. Consistent with the 1000 genomes phase 3 reference panel. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.


### 3.11 Results Subsection 11

Provided that all genomic data have been de-identified per gdpr article 89 standards. As determined by logistic regression with genomic principal components as covariates. Provided that all genomic data have been de-identified per gdpr article 89 standards. In a manner reasonably calculated to achieve reproducibility and open-science norms. As confirmed by cross-validation on held-out ancestry-stratified test sets.

Without prejudice to any obligations arising under the multi-party data sharing mou. Consistent with accepted practice for cross-ancestry polygenic score transferability. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the data monitoring committee's most recent data integrity review. Consistent with accepted practice for cross-ancestry polygenic score transferability.

In compliance with the fair data principles for genomic data sharing. Consistent with the data monitoring committee's most recent data integrity review. Pursuant to the data transfer agreement executed between the three institutions. In furtherance of the reproducibility objectives set out in the joint research plan. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.


### 3.12 Results Subsection 12

Consistent with accepted practice for cross-ancestry polygenic score transferability. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As confirmed by cross-validation on held-out ancestry-stratified test sets. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to the limitations prescribed by the cohort-specific consent agreements.

In accordance with gwas best-practice guidelines for multi-ancestry imputation. As specified in the approved data management plan filed with each home institution. Pursuant to the data transfer agreement executed between the three institutions. Consistent with the 1000 genomes phase 3 reference panel. As determined by logistic regression with genomic principal components as covariates.

As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review. Subject to the limitations prescribed by the cohort-specific consent agreements. As determined by logistic regression with genomic principal components as covariates. Consistent with the data monitoring committee's most recent data integrity review.


### 3.13 Results Subsection 13

Consistent with the data monitoring committee's most recent data integrity review. Provided that all genomic data have been de-identified per gdpr article 89 standards. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the 1000 genomes phase 3 reference panel. Subject to meta-analysis using metal with heterogeneity correction (cochran q).

As determined by logistic regression with genomic principal components as covariates. Without prejudice to any obligations arising under the multi-party data sharing mou. As determined by logistic regression with genomic principal components as covariates. Subject to meta-analysis using metal with heterogeneity correction (cochran q). In a manner reasonably calculated to achieve reproducibility and open-science norms.

In furtherance of the reproducibility objectives set out in the joint research plan. Consistent with the data monitoring committee's most recent data integrity review. Subject to the limitations prescribed by the cohort-specific consent agreements. As specified in the approved data management plan filed with each home institution. In furtherance of the reproducibility objectives set out in the joint research plan.


### 3.14 Results Subsection 14

As may be refined by subsequent protocol amendments issued by the coordinating pi. Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with accepted practice for cross-ancestry polygenic score transferability. In furtherance of the reproducibility objectives set out in the joint research plan. Provided that all genomic data have been de-identified per gdpr article 89 standards.

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As determined by logistic regression with genomic principal components as covariates. Following linkage-disequilibrium clumping with r² threshold of 0.1.

Pursuant to the data transfer agreement executed between the three institutions. Consistent with accepted practice for cross-ancestry polygenic score transferability. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to the limitations prescribed by the cohort-specific consent agreements. In compliance with the fair data principles for genomic data sharing.


### 3.15 Results Subsection 15

Pursuant to the data transfer agreement executed between the three institutions. Pursuant to the data transfer agreement executed between the three institutions. Consistent with the data monitoring committee's most recent data integrity review. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In a manner reasonably calculated to achieve reproducibility and open-science norms.

As specified in the approved data management plan filed with each home institution. As confirmed by cross-validation on held-out ancestry-stratified test sets. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Following linkage-disequilibrium clumping with r² threshold of 0.1. Pursuant to the data transfer agreement executed between the three institutions.

Subject to meta-analysis using metal with heterogeneity correction (cochran q). As determined by logistic regression with genomic principal components as covariates. In furtherance of the reproducibility objectives set out in the joint research plan. In compliance with the fair data principles for genomic data sharing. Subject to meta-analysis using metal with heterogeneity correction (cochran q).


### 3.16 Results Subsection 16

In accordance with gwas best-practice guidelines for multi-ancestry imputation. Subject to the limitations prescribed by the cohort-specific consent agreements. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Subject to the limitations prescribed by the cohort-specific consent agreements. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As validated by the polygenic risk score benchmarking framework pgs catalog v2. Consistent with the data monitoring committee's most recent data integrity review.

Following linkage-disequilibrium clumping with r² threshold of 0.1. In accordance with gwas best-practice guidelines for multi-ancestry imputation. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Consistent with the data monitoring committee's most recent data integrity review.


### 3.17 Results Subsection 17

Consistent with the data monitoring committee's most recent data integrity review. Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with accepted practice for cross-ancestry polygenic score transferability. In compliance with the fair data principles for genomic data sharing. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with the data monitoring committee's most recent data integrity review. Following linkage-disequilibrium clumping with r² threshold of 0.1. Consistent with the 1000 genomes phase 3 reference panel. Without prejudice to any obligations arising under the multi-party data sharing mou.

Consistent with the data monitoring committee's most recent data integrity review. Consistent with the 1000 genomes phase 3 reference panel. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As validated by the polygenic risk score benchmarking framework pgs catalog v2.


## 4. Discussion

The results of this multi-cohort validation study demonstrate that cross-ancestry PRS for T2D,
built on harmonized multi-cohort GWAS summary statistics and calibrated using ancestry-stratified
approaches, achieve meaningful improvement in predictive performance across diverse populations.



As validated by the polygenic risk score benchmarking framework pgs catalog v2. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Consistent with the 1000 genomes phase 3 reference panel. As determined by logistic regression with genomic principal components as covariates. Following linkage-disequilibrium clumping with r² threshold of 0.1.

Subject to the limitations prescribed by the cohort-specific consent agreements. As may be refined by subsequent protocol amendments issued by the coordinating pi. As confirmed by cross-validation on held-out ancestry-stratified test sets. As confirmed by cross-validation on held-out ancestry-stratified test sets. As confirmed by cross-validation on held-out ancestry-stratified test sets. As determined by logistic regression with genomic principal components as covariates.


As specified in the approved data management plan filed with each home institution. Without prejudice to any obligations arising under the multi-party data sharing mou. Provided that all genomic data have been de-identified per gdpr article 89 standards. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to meta-analysis using metal with heterogeneity correction (cochran q). In a manner reasonably calculated to achieve reproducibility and open-science norms.

As may be refined by subsequent protocol amendments issued by the coordinating pi. Subject to meta-analysis using metal with heterogeneity correction (cochran q). In a manner reasonably calculated to achieve reproducibility and open-science norms. As confirmed by cross-validation on held-out ancestry-stratified test sets. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). As confirmed by cross-validation on held-out ancestry-stratified test sets.


Following linkage-disequilibrium clumping with r² threshold of 0.1. Pursuant to the data transfer agreement executed between the three institutions. Pursuant to the data transfer agreement executed between the three institutions. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with the 1000 genomes phase 3 reference panel. In compliance with the fair data principles for genomic data sharing.

As determined by logistic regression with genomic principal components as covariates. In compliance with the fair data principles for genomic data sharing. Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with the 1000 genomes phase 3 reference panel. In compliance with the fair data principles for genomic data sharing. In accordance with gwas best-practice guidelines for multi-ancestry imputation.


As may be refined by subsequent protocol amendments issued by the coordinating pi. Provided that all genomic data have been de-identified per gdpr article 89 standards. As confirmed by cross-validation on held-out ancestry-stratified test sets. Consistent with the data monitoring committee's most recent data integrity review. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

As determined by logistic regression with genomic principal components as covariates. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Subject to meta-analysis using metal with heterogeneity correction (cochran q). Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with the 1000 genomes phase 3 reference panel. As determined by logistic regression with genomic principal components as covariates.


Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In a manner reasonably calculated to achieve reproducibility and open-science norms. Pursuant to the data transfer agreement executed between the three institutions. As may be refined by subsequent protocol amendments issued by the coordinating pi. Following linkage-disequilibrium clumping with r² threshold of 0.1. Subject to the limitations prescribed by the cohort-specific consent agreements.

As determined by logistic regression with genomic principal components as covariates. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As validated by the polygenic risk score benchmarking framework pgs catalog v2. Consistent with the 1000 genomes phase 3 reference panel. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).


In compliance with the fair data principles for genomic data sharing. Subject to meta-analysis using metal with heterogeneity correction (cochran q). As confirmed by cross-validation on held-out ancestry-stratified test sets. In a manner reasonably calculated to achieve reproducibility and open-science norms. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Provided that all genomic data have been de-identified per gdpr article 89 standards.

Following linkage-disequilibrium clumping with r² threshold of 0.1. Provided that all genomic data have been de-identified per gdpr article 89 standards. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Without prejudice to any obligations arising under the multi-party data sharing mou. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. As specified in the approved data management plan filed with each home institution.


Subject to the limitations prescribed by the cohort-specific consent agreements. Consistent with the data monitoring committee's most recent data integrity review. Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with the 1000 genomes phase 3 reference panel. As confirmed by cross-validation on held-out ancestry-stratified test sets. Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01).

As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with accepted practice for cross-ancestry polygenic score transferability. As confirmed by cross-validation on held-out ancestry-stratified test sets. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Consistent with the 1000 genomes phase 3 reference panel.


As determined by logistic regression with genomic principal components as covariates. In a manner reasonably calculated to achieve reproducibility and open-science norms. In a manner reasonably calculated to achieve reproducibility and open-science norms. In accordance with gwas best-practice guidelines for multi-ancestry imputation. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. In a manner reasonably calculated to achieve reproducibility and open-science norms.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). In compliance with the fair data principles for genomic data sharing. Consistent with the data monitoring committee's most recent data integrity review. As specified in the approved data management plan filed with each home institution. Provided that all genomic data have been de-identified per gdpr article 89 standards. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure.


In compliance with the fair data principles for genomic data sharing. In a manner reasonably calculated to achieve reproducibility and open-science norms. As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review. Consistent with the 1000 genomes phase 3 reference panel. Consistent with the data monitoring committee's most recent data integrity review.

In furtherance of the reproducibility objectives set out in the joint research plan. As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with accepted practice for cross-ancestry polygenic score transferability. Consistent with accepted practice for cross-ancestry polygenic score transferability. Following linkage-disequilibrium clumping with r² threshold of 0.1. In compliance with the fair data principles for genomic data sharing.


Consistent with accepted practice for cross-ancestry polygenic score transferability. As may be refined by subsequent protocol amendments issued by the coordinating pi. Consistent with the data monitoring committee's most recent data integrity review. Subject to meta-analysis using metal with heterogeneity correction (cochran q). Without prejudice to any obligations arising under the multi-party data sharing mou. Subject to the limitations prescribed by the cohort-specific consent agreements.

Subject to rigorous quality-control filters (info score > 0.8, maf > 0.01). Provided that all genomic data have been de-identified per gdpr article 89 standards. Consistent with the 1000 genomes phase 3 reference panel. Consistent with accepted practice for cross-ancestry polygenic score transferability. Taking into account trans-ethnic heterogeneity in linkage-disequilibrium structure. Consistent with accepted practice for cross-ancestry polygenic score transferability.


## 5. Conclusion

This study provides a validated cross-ancestry PRS pipeline for T2D risk prediction. The
harmonised datasets generated under this collaboration, subject to the data-sharing terms
agreed among the three institutions, provide a foundation for further cross-ancestry
genomics research.

## Acknowledgements

The authors acknowledge the contributions of all cohort participants. This work was conducted
under IRB-2024-GWAS-001 with oversight from Dr. Fatima Al-Rashid. Data harmonisation work was carried out by
Mina Takahashi (University of Toronto).
