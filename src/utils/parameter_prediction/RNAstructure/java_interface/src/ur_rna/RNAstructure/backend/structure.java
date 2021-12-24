/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 3.0.12
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package ur_rna.RNAstructure.backend;

public class structure {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected structure(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(structure obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RNABackendJNI.delete_structure(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public structure(int structures) {
    this(RNABackendJNI.new_structure__SWIG_0(structures), true);
  }

  public structure() {
    this(RNABackendJNI.new_structure__SWIG_1(), true);
  }

  public String GetCtLabel(int structurenumber) {
    return RNABackendJNI.structure_GetCtLabel(swigCPtr, this, structurenumber);
  }

  public int GetEnergy(int structurenumber) {
    return RNABackendJNI.structure_GetEnergy(swigCPtr, this, structurenumber);
  }

  public int GetNumberofStructures() {
    return RNABackendJNI.structure_GetNumberofStructures(swigCPtr, this);
  }

  public int GetPair(int i, int structurenumber) {
    return RNABackendJNI.structure_GetPair__SWIG_0(swigCPtr, this, i, structurenumber);
  }

  public int GetPair(int i) {
    return RNABackendJNI.structure_GetPair__SWIG_1(swigCPtr, this, i);
  }

  public int GetBase(int i) {
    return RNABackendJNI.structure_GetBase(swigCPtr, this, i);
  }

  public String GetSequenceLabel() {
    return RNABackendJNI.structure_GetSequenceLabel(swigCPtr, this);
  }

  public int GetSequenceLength() {
    return RNABackendJNI.structure_GetSequenceLength(swigCPtr, this);
  }

  public String GetSequence() {
    return RNABackendJNI.structure_GetSequence(swigCPtr, this);
  }

  public void RemovePair(int i, int structurenumber) {
    RNABackendJNI.structure_RemovePair__SWIG_0(swigCPtr, this, i, structurenumber);
  }

  public void RemovePair(int i) {
    RNABackendJNI.structure_RemovePair__SWIG_1(swigCPtr, this, i);
  }

  public boolean HasPseudoknots(int structurenumber) {
    return RNABackendJNI.structure_HasPseudoknots__SWIG_0(swigCPtr, this, structurenumber);
  }

  public boolean HasPseudoknots() {
    return RNABackendJNI.structure_HasPseudoknots__SWIG_1(swigCPtr, this);
  }

  public void FindPseudoknots(int structurenumber, CIntVector pseudoknotPairs, CIntVector normalPairs) {
    RNABackendJNI.structure_FindPseudoknots__SWIG_0(swigCPtr, this, structurenumber, CIntVector.getCPtr(pseudoknotPairs), pseudoknotPairs, CIntVector.getCPtr(normalPairs), normalPairs);
  }

  public void FindPseudoknots(int structurenumber, CIntVector pseudoknotPairs) {
    RNABackendJNI.structure_FindPseudoknots__SWIG_1(swigCPtr, this, structurenumber, CIntVector.getCPtr(pseudoknotPairs), pseudoknotPairs);
  }

  public void FindPseudoknots(int structurenumber) {
    RNABackendJNI.structure_FindPseudoknots__SWIG_2(swigCPtr, this, structurenumber);
  }

  public void GetPseudoknotRanks(CIntVector results, int structurenumber) {
    RNABackendJNI.structure_GetPseudoknotRanks__SWIG_0(swigCPtr, this, CIntVector.getCPtr(results), results, structurenumber);
  }

  public void GetPseudoknotRanks(CIntVector results) {
    RNABackendJNI.structure_GetPseudoknotRanks__SWIG_1(swigCPtr, this, CIntVector.getCPtr(results), results);
  }

  public void BreakPseudoknots(int structurenumber) {
    RNABackendJNI.structure_BreakPseudoknots(swigCPtr, this, structurenumber);
  }

  public void SetCtLabel(String label, int structurenumber) {
    RNABackendJNI.structure_SetCtLabel(swigCPtr, this, label, structurenumber);
  }

  public void SetEnergy(int structurenumber, int energy) {
    RNABackendJNI.structure_SetEnergy(swigCPtr, this, structurenumber, energy);
  }

  public void SetPair(int i, int j, int structurenumber) {
    RNABackendJNI.structure_SetPair__SWIG_0(swigCPtr, this, i, j, structurenumber);
  }

  public void SetPair(int i, int j) {
    RNABackendJNI.structure_SetPair__SWIG_1(swigCPtr, this, i, j);
  }

  public void SetSequenceLabel(String label) {
    RNABackendJNI.structure_SetSequenceLabel(swigCPtr, this, label);
  }

  public int SetSequence(String sequence) {
    return RNABackendJNI.structure_SetSequence(swigCPtr, this, sequence);
  }

  public void allocatetem() {
    RNABackendJNI.structure_allocatetem(swigCPtr, this);
  }

  public void AddDouble(int i) {
    RNABackendJNI.structure_AddDouble(swigCPtr, this, i);
  }

  public void AddForbiddenPair(int i, int j) {
    RNABackendJNI.structure_AddForbiddenPair(swigCPtr, this, i, j);
  }

  public void AddGUPair(int i) {
    RNABackendJNI.structure_AddGUPair(swigCPtr, this, i);
  }

  public void AddModified(int i) {
    RNABackendJNI.structure_AddModified(swigCPtr, this, i);
  }

  public void AddPair(int i, int j) {
    RNABackendJNI.structure_AddPair(swigCPtr, this, i, j);
  }

  public void AddSingle(int i) {
    RNABackendJNI.structure_AddSingle(swigCPtr, this, i);
  }

  public void AddDomain(int i, int j) {
    RNABackendJNI.structure_AddDomain(swigCPtr, this, i, j);
  }

  public boolean DistanceLimited() {
    return RNABackendJNI.structure_DistanceLimited(swigCPtr, this);
  }

  public int GetDouble(int i) {
    return RNABackendJNI.structure_GetDouble(swigCPtr, this, i);
  }

  public int GetForbiddenPair5(int i) {
    return RNABackendJNI.structure_GetForbiddenPair5(swigCPtr, this, i);
  }

  public int GetForbiddenPair3(int i) {
    return RNABackendJNI.structure_GetForbiddenPair3(swigCPtr, this, i);
  }

  public int GetGUpair(int i) {
    return RNABackendJNI.structure_GetGUpair(swigCPtr, this, i);
  }

  public int GetModified(int i) {
    return RNABackendJNI.structure_GetModified(swigCPtr, this, i);
  }

  public int GetNumberofDoubles() {
    return RNABackendJNI.structure_GetNumberofDoubles(swigCPtr, this);
  }

  public int GetNumberofForbiddenPairs() {
    return RNABackendJNI.structure_GetNumberofForbiddenPairs(swigCPtr, this);
  }

  public int GetNumberofGU() {
    return RNABackendJNI.structure_GetNumberofGU(swigCPtr, this);
  }

  public int GetNumberofModified() {
    return RNABackendJNI.structure_GetNumberofModified(swigCPtr, this);
  }

  public int GetNumberofSingles() {
    return RNABackendJNI.structure_GetNumberofSingles(swigCPtr, this);
  }

  public int GetNumberofPairs() {
    return RNABackendJNI.structure_GetNumberofPairs(swigCPtr, this);
  }

  public int GetNumberofDomains() {
    return RNABackendJNI.structure_GetNumberofDomains(swigCPtr, this);
  }

  public int GetPair5(int i) {
    return RNABackendJNI.structure_GetPair5(swigCPtr, this, i);
  }

  public int GetPair3(int i) {
    return RNABackendJNI.structure_GetPair3(swigCPtr, this, i);
  }

  public int GetPairingDistanceLimit() {
    return RNABackendJNI.structure_GetPairingDistanceLimit(swigCPtr, this);
  }

  public int GetSingle(int i) {
    return RNABackendJNI.structure_GetSingle(swigCPtr, this, i);
  }

  public void RemoveSingleStrandConstraints(int number) {
    RNABackendJNI.structure_RemoveSingleStrandConstraints(swigCPtr, this, number);
  }

  public int GetDomain5(int i) {
    return RNABackendJNI.structure_GetDomain5(swigCPtr, this, i);
  }

  public int GetDomain3(int i) {
    return RNABackendJNI.structure_GetDomain3(swigCPtr, this, i);
  }

  public void RemoveConstraints() {
    RNABackendJNI.structure_RemoveConstraints(swigCPtr, this);
  }

  public void SetPairingDistance(int maxdistance) {
    RNABackendJNI.structure_SetPairingDistance(swigCPtr, this, maxdistance);
  }

  public int ctout(String ctoutfile) {
    return RNABackendJNI.structure_ctout(swigCPtr, this, ctoutfile);
  }

  public int writedotbracket(String filename, int structurenumber, DotBracketFormat format) {
    return RNABackendJNI.structure_writedotbracket__SWIG_0(swigCPtr, this, filename, structurenumber, format.swigValue());
  }

  public int writedotbracket(String filename, int structurenumber) {
    return RNABackendJNI.structure_writedotbracket__SWIG_1(swigCPtr, this, filename, structurenumber);
  }

  public int writedotbracket(String filename) {
    return RNABackendJNI.structure_writedotbracket__SWIG_2(swigCPtr, this, filename);
  }

  public int openct(String ctfile) {
    return RNABackendJNI.structure_openct(swigCPtr, this, ctfile);
  }

  public int opendbn(String bracketFile) {
    return RNABackendJNI.structure_opendbn(swigCPtr, this, bracketFile);
  }

  public int writeseq(String seqfile, int seqFileType, boolean append) {
    return RNABackendJNI.structure_writeseq__SWIG_0(swigCPtr, this, seqfile, seqFileType, append);
  }

  public int writeseq(String seqfile, int seqFileType) {
    return RNABackendJNI.structure_writeseq__SWIG_1(swigCPtr, this, seqfile, seqFileType);
  }

  public int writeseq(String seqfile) {
    return RNABackendJNI.structure_writeseq__SWIG_2(swigCPtr, this, seqfile);
  }

  public int openseq(String seqfile) {
    return RNABackendJNI.structure_openseq(swigCPtr, this, seqfile);
  }

  public int openseqx(String seqfile) {
    return RNABackendJNI.structure_openseqx(swigCPtr, this, seqfile);
  }

  public void AddStructure() {
    RNABackendJNI.structure_AddStructure(swigCPtr, this);
  }

  public void CleanStructure(int structurenumber) {
    RNABackendJNI.structure_CleanStructure(swigCPtr, this, structurenumber);
  }

  public void RemoveLastStructure() {
    RNABackendJNI.structure_RemoveLastStructure(swigCPtr, this);
  }

  public void RemoveAllStructures() {
    RNABackendJNI.structure_RemoveAllStructures(swigCPtr, this);
  }

  public void RemoveStructure(int structurenumber) {
    RNABackendJNI.structure_RemoveStructure(swigCPtr, this, structurenumber);
  }

  public datatable GetThermodynamicDataTable() {
    long cPtr = RNABackendJNI.structure_GetThermodynamicDataTable(swigCPtr, this);
    return (cPtr == 0) ? null : new datatable(cPtr, false);
  }

  public void SetThermodynamicDataTable(datatable DataTablePointer) {
    RNABackendJNI.structure_SetThermodynamicDataTable(swigCPtr, this, datatable.getCPtr(DataTablePointer), DataTablePointer);
  }

  public boolean IsAlphabetLoaded() {
    return RNABackendJNI.structure_IsAlphabetLoaded(swigCPtr, this);
  }

  public boolean IsThermoDataLoaded() {
    return RNABackendJNI.structure_IsThermoDataLoaded(swigCPtr, this);
  }

  public void sort() {
    RNABackendJNI.structure_sort(swigCPtr, this);
  }

  public boolean ProblemwithStructures() {
    return RNABackendJNI.structure_ProblemwithStructures(swigCPtr, this);
  }

  public int ReadSHAPE(String filename, float SingleStrandThreshold, float ModificationThreshold) {
    return RNABackendJNI.structure_ReadSHAPE__SWIG_0(swigCPtr, this, filename, SingleStrandThreshold, ModificationThreshold);
  }

  public int ReadSHAPE(String filename, RestraintType modifier, boolean calculatePseudoEnergies) {
    return RNABackendJNI.structure_ReadSHAPE__SWIG_1(swigCPtr, this, filename, modifier.swigValue(), calculatePseudoEnergies);
  }

  public int ReadSHAPE(String filename, RestraintType modifier) {
    return RNABackendJNI.structure_ReadSHAPE__SWIG_2(swigCPtr, this, filename, modifier.swigValue());
  }

  public int ReadSHAPE(String filename) {
    return RNABackendJNI.structure_ReadSHAPE__SWIG_3(swigCPtr, this, filename);
  }

  public int ReadOffset(String SSOffset, String DSOffset) {
    return RNABackendJNI.structure_ReadOffset(swigCPtr, this, SSOffset, DSOffset);
  }

  public int ReadExperimentalPairBonus(String filename, double experimentalOffset, double experimentalScaling) {
    return RNABackendJNI.structure_ReadExperimentalPairBonus__SWIG_0(swigCPtr, this, filename, experimentalOffset, experimentalScaling);
  }

  public int ReadExperimentalPairBonus(String filename, double experimentalOffset) {
    return RNABackendJNI.structure_ReadExperimentalPairBonus__SWIG_1(swigCPtr, this, filename, experimentalOffset);
  }

  public int ReadExperimentalPairBonus(String filename) {
    return RNABackendJNI.structure_ReadExperimentalPairBonus__SWIG_2(swigCPtr, this, filename);
  }

  public int WriteSHAPE(String outfile, boolean printHeaders) {
    return RNABackendJNI.structure_WriteSHAPE__SWIG_0(swigCPtr, this, outfile, printHeaders);
  }

  public int WriteSHAPE(String outfile) {
    return RNABackendJNI.structure_WriteSHAPE__SWIG_1(swigCPtr, this, outfile);
  }

  public void DeleteSHAPE() {
    RNABackendJNI.structure_DeleteSHAPE(swigCPtr, this);
  }

  public void AllocateSHAPE() {
    RNABackendJNI.structure_AllocateSHAPE(swigCPtr, this);
  }

  public void allocateconstant() {
    RNABackendJNI.structure_allocateconstant(swigCPtr, this);
  }

  public void setSHAPEFileRead(boolean value) {
    RNABackendJNI.structure_SHAPEFileRead_set(swigCPtr, this, value);
  }

  public boolean getSHAPEFileRead() {
    return RNABackendJNI.structure_SHAPEFileRead_get(swigCPtr, this);
  }

  public String GetErrorDetails() {
    return RNABackendJNI.structure_GetErrorDetails(swigCPtr, this);
  }

  public boolean IsNuc(int i, char c) {
    return RNABackendJNI.structure_IsNuc__SWIG_0(swigCPtr, this, i, c);
  }

  public boolean IsNuc(int i, char c, datatable data) {
    return RNABackendJNI.structure_IsNuc__SWIG_1(swigCPtr, this, i, c, datatable.getCPtr(data), data);
  }

  public void RemoveEnergyLabels(String customLabel) {
    RNABackendJNI.structure_RemoveEnergyLabels__SWIG_0(swigCPtr, this, customLabel);
  }

  public void RemoveEnergyLabels() {
    RNABackendJNI.structure_RemoveEnergyLabels__SWIG_1(swigCPtr, this);
  }

  public SWIGTYPE_p_int generate_constraint_matrix() {
    long cPtr = RNABackendJNI.structure_generate_constraint_matrix(swigCPtr, this);
    return (cPtr == 0) ? null : new SWIGTYPE_p_int(cPtr, false);
  }

  public static void setShowWarnings(int value) {
    RNABackendJNI.structure_ShowWarnings_set(value);
  }

  public static int getShowWarnings() {
    return RNABackendJNI.structure_ShowWarnings_get();
  }

  public static void setSumShapeRepeats(boolean value) {
    RNABackendJNI.structure_SumShapeRepeats_set(value);
  }

  public static boolean getSumShapeRepeats() {
    return RNABackendJNI.structure_SumShapeRepeats_get();
  }

}
