import cyvcf2
import os, sys
import numpy as np
import pytest

import trtools.utils.mergeutils as mergeutils
import trtools.utils.tr_harmonizer as trh


@pytest.fixture
def mrgvcfdir(vcfdir):
	return os.path.join(vcfdir, "mergeSTR_vcfs")

# Set up dummy class
class DummyRecord:
    def __init__(self, chrom, pos, ref, alts=[], info = {}):
        self.CHROM = chrom
        self.POS = pos
        self.REF = ref
        self.ALTS = alts
        self.INFO = info

def test_DebugPrintRecordLocations(capsys):
    dummy_records = [] 
    dummy_records.append(DummyRecord('chr1', 100, 'CAGCAG', info={'END': 120}))
    dummy_records.append(DummyRecord('chr1', 150, 'CTTCTT', info={'END': 170}))
    
    mergeutils.DebugPrintRecordLocations(dummy_records, [True, False])
    captured = capsys.readouterr()
    assert "chr1:100:True" in captured.err
    assert "chr1:150:False" in captured.err

def test_CheckMin():
    assert mergeutils.CheckMin([True, False]) == False
    with pytest.raises(ValueError) as info:
        mergeutils.CheckMin([False, False])
    assert "Unexpected error. Stuck in infinite loop and exiting." in str(info.value)

def test_CheckVCFType(vcfdir):
    snps_path = os.path.join(vcfdir, "snps.vcf")
    gangstr_path = os.path.join(vcfdir, "test_gangstr.vcf")
    hipstr_path = os.path.join(vcfdir, "test_hipstr.vcf")
    gangstr_vcf = cyvcf2.VCF(gangstr_path)
    hipstr_vcf = cyvcf2.VCF(hipstr_path)
    snps_vcf = cyvcf2.VCF(snps_path)
    # TODO add tests to infer vcf type
    assert trh.VcfTypes.gangstr == mergeutils.GetAndCheckVCFType([gangstr_vcf], "gangstr")

    with pytest.raises(ValueError) as info:
        print(mergeutils.GetAndCheckVCFType([gangstr_vcf, hipstr_vcf], "auto"))
    assert "VCF files are of mixed types." in str(info.value)
    
    with pytest.raises(TypeError) as info:
        print(mergeutils.GetAndCheckVCFType([gangstr_vcf, snps_vcf], "auto"))
    assert "Could not identify the type of this vcf" in str(info.value)

# Test no such file or directory
def test_WrongFile(mrgvcfdir):
    # Try a dummy file name. Make sure it doesn't exist before we try
    fname1 = os.path.join(mrgvcfdir, "test_non_existent1.vcf.gz")
    fname2 = os.path.join(mrgvcfdir, "test_non_existent2.vcf.gz")
    if os.path.exists(fname1):
        os.remove(fname1)
    if os.path.exists(fname2):
        os.remove(fname2)
    print (os.path.isfile(fname1))
    with pytest.raises(ValueError) as info:
        mergeutils.LoadReaders([fname1, fname2])
    assert "Could not find VCF file" in str(info.value)

# test unzipped, unindexed VCFs return 1
def test_UnzippedUnindexedFile(mrgvcfdir):
    fname1 = os.path.join(mrgvcfdir, "test_file_gangstr_unzipped1.vcf")
    fname2 = os.path.join(mrgvcfdir, "test_file_gangstr_unzipped2.vcf")
    with pytest.raises(ValueError) as info:
        mergeutils.LoadReaders([fname1, fname2])
    assert "is bgzipped and indexed" in str(info.value)

    fname1 = os.path.join(mrgvcfdir, "test_file_gangstr_unindexed1.vcf.gz")
    fname2 = os.path.join(mrgvcfdir, "test_file_gangstr_unindexed2.vcf.gz")
    with pytest.raises(ValueError) as info:
        mergeutils.LoadReaders([fname1, fname2])
    assert "Could not find VCF index" in str(info.value)
