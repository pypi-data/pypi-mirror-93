# nCoV_minipipe aka CovPipe

[![pipeline status](https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/badges/master/pipeline.svg)](https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/-/commits/master)
[![Snakemake](https://img.shields.io/badge/snakemake-≥5.26.0-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)

[[_TOC_]]

## 1. Introduction

CovPipe provides a fully automated, flexible and reproducible workflow for reconstructing genome sequences from NGS data based on a given reference sequence (see section 5 for more details). The pipeline is optimized for SARS-CoV-2 data, but can also be used for other viruses.


## 2. Setup

### 2.1 Quick manual Setup

The most convenient way to install the pipeline is by using git and [conda](https://docs.conda.io/en/latest/miniconda.html):

```bash
# installing the pipeline using git
cd designated/path
git clone https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe.git
cd ncov_minipipe
```
There are currently two ways of installing the pipeline

#### 2.1.1 (Option 1) Manually installing with conda and pip (recommended) 

```bash
conda install -c bioconda python -mn covpipe_env # You can also use skip the creation and 
. activate covpipe_env                           # only activate a existing environment here. 
python -m pip install .                          # Running this line alone installs it in the current environment or globally
ncov_minipipe --help
```

#### 2.1.2 (Option 2) Running the setup script

```bash 
# installing software dependencies using conda
ncov_minipipe/ncov_minipipe.conda.setup/setup_env.sh
. activate covpipe_environment/
ncov_minipipe --help
```

### 2.2 Manual Setup

Download the pipeline from https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/-/releases
and extract the content of the downloaded archive to the designated path.

Make sure that the following dependencies are available on your system and added to the system's PATH variable before running the pipeline:

| Dependencies | version |
| ------------ | ------- |
| [python](https://www.python.org/downloads/) | 3.6.0+ |
| [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) | 5.26+ |
| [strictyaml](https://pypi.org/project/strictyaml/) | 1.0.6 |
| [biopython](https://biopython.org/) | 1.7.8 |
| [pandas](https://pypi.org/project/pandas/) | 1.1.4 |
| [singularity](https://singularity.lbl.gov/) | 3.6.0 |

### 2.3 Test

The pipeline setup can quickly be tested using:

```bash
designated/path/ncov_minipipe/tests/quicktest.sh
```

# 3. Usage

As a minimum the pipeline needs the following input:
- FASTA file containing one reference sequence (`--reference`)
- folder containing gz-compressed FASTQ files (`--input`)
- output folder (`-o`), in which a subfolder named results is created to store all results

```bash
# activate conda environment once before using the pipeline (only applicable if software dependencies were installed according to section 2.1)
conda activate path/to/covPipe/covpipe_environment/ 

# thoughtless run (no primer and adapater-clipping and no taxonomic read filtering)
ncov_minipipe --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```

# 4. Options to Customize the Workflow

The manual page provides information on all options available.

```bash
ncov_minipipe --help
```

## 4.1 Activating Adapter Clipping

Adapter sequences can be clipped to prevent mis-alignments to the reference sequence. For this purpose you must provide a FASTA file
containing the adapter sequences (`--adapter`).
If you provide the option a name like "Nextera", it will get a matching file from pipeline internals.  

It defaults to NexteraTransposase Adpaters by Illumina  (**Oligonucleotide sequences © 2020 Illumina, Inc. All rights reserved**)

```bash
# clipping adapter sequences listed in myAdapterfileFile.fasta
ncov_minipipe --adapter path/to/myAdapterfileFile.fasta
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder 
```

## 4.2 Activating Primer Clipping

If needed, amplicon primers can be cut off to prevent masking of variants by those. 
For this purpose, a bedpe file has to be provided that contains the following information as tab-delimited fields (`--primer`):

1. field: forward primer chromosome name
2. field: forward primer start position
3. field: forward primer end position
4. field: reverse primer chromosome
5. field: reverse primer start position
6. field: reverse primer end position
7. field: auxiliary information

Example:

> NC_045512.2     333     350     NC_045512.2     450     470     Amplicon1
>
> NC_045512.2     876     899     NC_045512.2     995     1005    Amplicon2


```bash
# clipping primer sequences listed in myPrimerPositions.bedpe
ncov_minipipe --primer path/to/myPrimerPositions.bedpe \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```
### 4.2.1 Create bedpe from amplicon bed file

Sometimes you do not have access to a bed file with primer positions.
If you only have a bedfile with amplicon start and end positions and
the same for the inserts, you can transform this into the desired bed file.

```bash
create_bedpe AMPLICON_FILE.bed INSERT_FILE.bed -o myPrimerPositions.bedpe
```


## 4.3 Activating taxonomic Read Filtering

If necessary, reads not derived from SARS-COV-2 can be excluded. 
Read classification is based on corresponding k-mer frequencies using a defined kraken2 database (`--krakenDb`). 
A pre-processed database containing SARS-CoV2 and human genome sequences can be downloaded from: 

https://zenodo.org/record/3854856 


If you are not working on SARS-COV-2, the target taxonomy ID  can be changed (option `--taxid`; default: 2697049 = SARS-COV-2).

```bash
# including reads that can be assigned to SARS-COV-2 (taxonomy id: 2697049) using the kraken2 database in myKrakenDbFolder 
ncov_minipipe --krakenDb path/to/myKrakenDbFolder \
              --taxid 2697049 \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```

## 4.4 Adapting Variant Calling

Sites considered for variant calling can be restricted based on the following parameters at the respective position.

- the minimum sequencing depth (`--var_call_cov`; default: 20) 
- the minimum number of reads supporting a variant (`--var_call_count`; default: 10)
- the relative number of reads supporting a variant (`--var_call_frac`; default: 0.1) 

```bash
# excluding sites covered by less than 20 reads or less than 5 or 10% reads supporting a variant at this site
ncov_minipipe --var_call_cov 20 \
              --var_call_count 5 \
              --var_call_frac 0.1 \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```

## 4.5 Adapting Variant Filtering

Variants can be excluded, if the mean mapping quality of observed alternate alleles does not meet a given threshold (`--var_filter_mqm`; default: 40).
The mapping quality measures how good reads align to the respective reference genome region. Good mapping qualities are around MQ 60. 

Additionally, variants can be filtered if the strand balance probability for the alternate allele exceeds a given threshold (`--var_filter_sap`; default: 60).
The strand balance probability is a Phred-scaled measure of strand bias. A value near 0 indicates little or no strand bias. 

Finally, variants can be filtered by the site quality (`--var_filter_qual`; default: 10) indicating the pobability for a polymorphism at the respictive site.


```bash
# excluding variants associated to a mean mapping quality below 40, a strand balance probability of more than 60 
# or a pobability for a polymorphism of less than 10 at the respective site
ncov_minipipe --var_filter_mqm 40 \
              --var_filter_sap 60 \
              --var_filter_qual 10 \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```

## 4.6 Adapting Consensus Generation

When generating the consensus sequence, all positions whose read coverage is below a defined threshold can be hard-masked by N (`--cns_min_cov`; default: 20). 
In addtion, genotypes can be adjusted meaning that variants supported by a given fraction of all reads covering the respective site are called explicitely (`--cns_gt_adjust`; default: 0.9). 
This means that a variant that shows a read fraction of 0.94 would be set to full alternate allele and variants showing only 0.03 readfraction are changed to reference.

```bash
# hard-masking sites covered by less than 10 reads and explicitely call variants
# supported by at least 95% of all reads at the respective site
ncov_minipipe --cns_min_cov 10 \
              --gt_adjust 0.95 \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder
```

## 4.7 Lineage assignment 

The generated consensus sequences can be submitted to a preliminary lineage assignment. 
This will run Pangolin on the IUPAC consensus sequence.

Please follow the setup instructions on the pangolin project site https://github.com/cov-lineages/pangolin.

If the pipeline is run using an older install of pangolin it could be that the assigned lineages are outdated. 
Please consider a detailed lineage assignment after running this pipeline

```bash
# preliminary lineage assignment
ncov_minipipe --pangolin path/to/pangolin_conda_environment \
              --reference path/to/myReference.fasta \
              --input path/to/myInputFolder \
              -o path/to/myOutputFolder

```

# 5 Workflow

![workflow](docs/workflow.png "workflow")

The illustration shows a slightly simplified workflow that can be divided into the following sections: 


## 5.1 Pre-processing

To ensure the quality of sequence data used for reconstruction, the workflow provides: 

steps: 
- 5' clipping of amplification primer sequences (optional)
- 3' removal of
  - Illumina adapter sequences (optional)
  - low complexity stretches
  - low quality stretches
- excluding of non-SARS-CoV-2 reads (optional)
  - to our experience this step improves analyses quality a lot and hence we recommend that

used tools:
- bamclipper
- fastp
- kraken2 

## 5.2 Mapping

Pre-processed Reads are aligned to the reference sequence using bwa-mem (default parameter).

## 5.3 Variant calling, filtering, genotype adjustment and annotation

Variants are called using freebayes allowing the following customizations:
  - minimal total coverage (`--var_call_cov`; default: 20) 
  - absolute number of variant supporting reads (`--var_call_count`; default: 10)
  - relative number of variant supporting reads (`--var_call_frac`; default: 0.1) 

The called variants can be further filtered using bcftools. For this custom thresholds can be applied to  
  - mean mapping quality of observed alternate alleles (MQM, `--var_filter_mqm`; default: 40)
  - strand balance probability for the alternate allele (SAP, `--var_filter_sap`; default: 60)
  - polymorphism probability (QUAL, `--var_filter_qual`; default: 10)

As unique feature the worklow allows to adjust the genotype of certain sites by explicitely calling variants supported by a given fraction of reads covering the respective site.

By default, all variants are inspected regarding their impact on coding sequences using SNPeff. 
This only works, if  your reference genome is listed in the SNPeff supported genomes (see Appendix below). Otherwise please deactivate this feature. (`--no-var-annotation`)


## 5.4 Consensus generation

Using bcftools the consensus is created allowing to mask lowly covered regions by N (user-defined threshold).
The default consensus (suffix iupac) follows iupac nomenclature at sites mixed variants have been detected 
(and were not adjusted by genotype as described before).
In addition, a second consensus is created for each dataset (suffix masked) where these ambiguous sites are
masked by N (additionally to the lowly covered regions).

## 5.5 Lineage assignment

Pangolin is used to establish a preliminary lineage assignment. (`--pangolin`)

## 5.6 QC-Report

In addition, to the consensus sequences a HTML-based report is generated summarizing different quality measures and mapping statistics for each dataset such as:

- runID (optional))
- conditional table that warns the user, if samples that were identified as negative controls show high reference genome coverage
- table of read properties:
  - number of bases (before / after trimming)
    - if amplification primer clipping was done
  - length of reads (before / after trimming)
    - if amplification primer clipping was done
  - number of bases mapped (Q = 30)
- optional table listing the species filtering results emitted by Kraken2
- table of mapping properties:
  - reads mapped to reference genome (number & fraction of input)
  - median / sd  of fragment size
- genome wide plot of coverage
- histogram of fragment sizes

- table of reference coverage characteristics
- table of lineage assigments using pangolin (optional)

Samples showing at least 20x sequencing depth at more than 95% of the reference genome are designated a successful genome sequencing.


# Troubleshoot

Please visit the [project's wiki ](https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/-/wikis/home) for further information.

# Do you feel like contributing?

This [link](https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/-/blob/edit_readme/CONTRIBUTING.md) will take you to our contribution guide

# Appendix

### SNPeff supported genomes

Listed are SARS-CoV-2 genomes supported by SNPeff.
Thanks to the Bioconda Team!

AP006557.1	SARS coronavirus TWH genomic RNA, complete genome.

AP006558.1	SARS coronavirus TWJ genomic RNA, complete genome.

AP006559.1	SARS coronavirus TWK genomic RNA, complete genome.

AP006560.1	SARS coronavirus TWS genomic RNA, complete genome.

AP006561.1	SARS coronavirus TWY genomic RNA, complete genome.

AY278488.2	SARS coronavirus BJ01, complete genome.

AY278489.2	SARS coronavirus GD01, complete genome.

AY278554.2	SARS coronavirus CUHK-W1, complete genome.

AY278741.1	SARS coronavirus Urbani, complete genome.

AY279354.2	SARS coronavirus BJ04, complete genome.

AY282752.2	SARS coronavirus CUHK-Su10, complete genome.

AY291451.1	SARS coronavirus TW1, complete genome.

AY304486.1	SARS coronavirus SZ3, complete genome.

AY304488.1	SARS coronavirus SZ16, complete genome.

AY304495.1	SARS coronavirus GZ50, complete genome.

AY310120.1	SARS coronavirus FRA, complete genome.

AY313906.1	SARS coronavirus GD69, complete genome.

AY323977.2	SARS coronavirus HSR 1, complete genome.

AY338174.1	SARS coronavirus Taiwan TC1, complete genome.

AY338175.1	SARS coronavirus Taiwan TC2, complete genome.

AY340092.1	SARS coronavirus BJ2232 RNA polymerase gene, partial cds.

AY345986.1	SARS coronavirus CUHK-AG01, complete genome.

AY345987.1	SARS coronavirus CUHK-AG02, complete genome.

AY345988.1	SARS coronavirus CUHK-AG03, complete genome.

AY348314.1	SARS coronavirus Taiwan TC3, complete genome.

AY350750.1	SARS coronavirus PUMC01, complete genome.

AY357075.1	SARS coronavirus PUMC02, complete genome.

AY357076.1	SARS coronavirus PUMC03, complete genome.

AY390556.1	SARS coronavirus GZ02, complete genome.

AY394978.1	SARS coronavirus GZ-B, complete genome.

AY394979.1	SARS coronavirus GZ-C, complete genome.

AY427439.1	SARS coronavirus AS, complete genome.

AY463059.1	SARS coronavirus ShanghaiQXC1, complete genome.

AY463060.1	SARS coronavirus ShanghaiQXC2, complete genome.

AY485277.1	SARS coronavirus Sino1-11, complete genome.

AY485278.1	SARS coronavirus Sino3-11, complete genome.

AY502923.1	SARS coronavirus TW10, complete genome.

AY502924.1	SARS coronavirus TW11, complete genome.

AY502925.1	SARS coronavirus TW2, complete genome.

AY502926.1	SARS coronavirus TW3, complete genome.

AY502927.1	SARS coronavirus TW4, complete genome.

AY502928.1	SARS coronavirus TW5, complete genome.

AY502929.1	SARS coronavirus TW6, complete genome.

AY502930.1	SARS coronavirus TW7, complete genome.

AY502931.1	SARS coronavirus TW8, complete genome.

AY502932.1	SARS coronavirus TW9, complete genome.

AY508724.1	SARS coronavirus NS-1, complete genome.

AY515512.1	SARS coronavirus HC/SZ/61/03, complete genome.

AY568539.1	SARS coronavirus GZ0401, complete genome.

AY572034.1	SARS coronavirus civet007, complete genome.

AY572035.1	SARS coronavirus civet010, complete genome.

AY572038.1	SARS coronavirus civet020, complete genome.

AY595412.1	SARS coronavirus LLJ-2004, complete genome.

AY613947.1	SARS coronavirus GZ0402, complete genome.

AY654624.1	SARS coronavirus TJF, complete genome.

AY686863.1	SARS coronavirus A022, complete genome.

AY686864.1	SARS coronavirus B039, complete genome.

AY687354.1	SARS coronavirus A001 spike glycoprotein gene, complete cds.

AY687355.1	SARS coronavirus A013 spike glycoprotein gene, complete cds.

AY687356.1	SARS coronavirus A021 spike glycoprotein gene, complete cds.

AY687357.1	SARS coronavirus A030 spike glycoprotein gene, complete cds.

AY687358.1	SARS coronavirus A031 spike glycoprotein gene, complete cds.

AY687359.1	SARS coronavirus B012 spike glycoprotein gene, complete cds.

AY687360.1	SARS coronavirus B024 spike glycoprotein gene, complete cds.

AY687361.1	SARS coronavirus B029 spike glycoprotein gene, complete cds.

AY687362.1	SARS coronavirus B033 spike glycoprotein gene, complete cds.

AY687364.1	SARS coronavirus B040 spike glycoprotein gene, complete cds.

AY714217.1	SARS Coronavirus CDC#200301157, complete genome.

AY772062.1	SARS coronavirus WH20, complete genome.

AY864805.1	SARS coronavirus BJ162, complete genome.

AY864806.1	SARS coronavirus BJ202, complete genome.

DQ022305.2	Bat SARS coronavirus HKU3-1, complete genome.

DQ084199.1	bat SARS coronavirus HKU3-2, complete genome.

DQ084200.1	bat SARS coronavirus HKU3-3, complete genome.

DQ182595.1	SARS coronavirus ZJ0301 from China, complete genome.

DQ640652.1	SARS coronavirus GDH-BJH01, complete genome.

DQ648856.1	Bat coronavirus (BtCoV/273/2005), complete genome.

DQ648857.1	Bat coronavirus (BtCoV/279/2005), complete genome.

EU371559.1	SARS coronavirus ZJ02, complete genome.

EU371560.1	SARS coronavirus BJ182a, complete genome.

EU371561.1	SARS coronavirus BJ182b, complete genome.

EU371562.1	SARS coronavirus BJ182-4, complete genome.

EU371563.1	SARS coronavirus BJ182-8, complete genome.

EU371564.1	SARS coronavirus BJ182-12, complete genome.

FJ882963.1	SARS coronavirus P2, complete genome.

GQ153539.1	Bat SARS coronavirus HKU3-4, complete genome.

GQ153540.1	Bat SARS coronavirus HKU3-5, complete genome.

GQ153541.1	Bat SARS coronavirus HKU3-6, complete genome.

GQ153542.1	Bat SARS coronavirus HKU3-7, complete genome.

GQ153543.1	Bat SARS coronavirus HKU3-8, complete genome.

GQ153544.1	Bat SARS coronavirus HKU3-9, complete genome.

GQ153545.1	Bat SARS coronavirus HKU3-10, complete genome.

GQ153546.1	Bat SARS coronavirus HKU3-11, complete genome.

GQ153547.1	Bat SARS coronavirus HKU3-12, complete genome.

JQ316196.1	SARS coronavirus HKU-39849 isolate UOB, complete genome.

JX993987.1	Bat coronavirus Rp/Shaanxi2011, complete genome.

JX993988.1	Bat coronavirus Cp/Yunnan2011, complete genome.

KC881005.1	Bat SARS-like coronavirus RsSHC014, complete genome.

KC881006.1	Bat SARS-like coronavirus Rs3367, complete genome.

KF367457.1	Bat SARS-like coronavirus WIV1, complete genome.

KF569996.1	Rhinolophus affinis coronavirus isolate LYRa11, complete genome.

KP886808.1	Bat SARS-like coronavirus YNLF_31C, complete genome.

KP886809.1	Bat SARS-like coronavirus YNLF_34C, complete genome.

MK062179.1	SARS coronavirus Urbani isolate icSARS, complete genome.

MK062180.1	SARS coronavirus Urbani isolate icSARS-MA, complete genome.

MK062181.1	SARS coronavirus Urbani isolate icSARS-C3, complete genome.

MK062182.1	SARS coronavirus Urbani isolate icSARS-C3-MA, complete genome.

MK062183.1	SARS coronavirus Urbani isolate icSARS-C7, complete genome.

MK062184.1	SARS coronavirus Urbani isolate icSARS-C7-MA, complete genome.

MN996532.1	Bat coronavirus RaTG13, complete genome.

NC_045512.2                                                 	COVID19 Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1
