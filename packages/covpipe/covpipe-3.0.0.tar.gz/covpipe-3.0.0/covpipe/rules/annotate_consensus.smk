singularity: "docker://rkibioinf/liftoff:1.5.1--78a2baa"

rule annotateAmbiguousConsensus:
    input:
        fasta = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.fasta"),
        annotation = CNS_ANNOT,
        ref = REFERENCE
    output:
        annotation_iupac = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.gff"),
        unmapped_features_iupac = os.path.join(IUPAC_CNS_FOLDER, "{sample}_unmapped_features_iupac_consensus.txt")
    log:
        os.path.join(DATAFOLDER["logs"], "annotate_ambiguous_consensus", "{sample}.log")
    conda:
        "../envs/liftoff.yaml"
    threads: 1
    shell:
        r"""
            liftoff -o {output.annotation_iupac} -u {output.unmapped_features_iupac} -g {input.annotation} {input.fasta} {input.ref} 2> {log}
        """

rule annotateMaskedConsensus:
    input:
        fasta = os.path.join(MASKED_CNS_FOLDER, "{sample}.masked_consensus.fasta"),
        annotation = CNS_ANNOT,
        ref = REFERENCE
    output:
        annotation_masked = os.path.join(MASKED_CNS_FOLDER, "{sample}.masked_consensus.gff"),
        unmapped_features_masked = os.path.join(MASKED_CNS_FOLDER, "{sample}_unmapped_features_masked_consensus.txt")
    log:
        os.path.join(DATAFOLDER["logs"], "annotate_masked_consensus", "{sample}.log")
    conda:
        "../envs/liftoff.yaml"
    threads: 1
    shell:
        r"""
            liftoff -o {output.annotation_masked} -u {output.unmapped_features_masked} -g {input.annotation} {input.fasta} {input.ref} 2> {log}
        """
