/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 3.0.12
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package ur_rna.RNAstructure.backend;

public class RNABackend implements RNABackendConstants {
  public static DotBracketFormat parseDotBracketFormat(String format) {
    return DotBracketFormat.swigToEnum(RNABackendJNI.parseDotBracketFormat(format));
  }

  public static boolean hasPseudoknots(CIntVector pairs) {
    return RNABackendJNI.hasPseudoknots(CIntVector.getCPtr(pairs), pairs);
  }

  public static void findPseudoknots(CIntVector currentPairs, CIntVector pseudoknotPairs, CIntVector normalPairs) {
    RNABackendJNI.findPseudoknots__SWIG_0(CIntVector.getCPtr(currentPairs), currentPairs, CIntVector.getCPtr(pseudoknotPairs), pseudoknotPairs, CIntVector.getCPtr(normalPairs), normalPairs);
  }

  public static void findPseudoknots(CIntVector currentPairs, CIntVector pseudoknotPairs) {
    RNABackendJNI.findPseudoknots__SWIG_1(CIntVector.getCPtr(currentPairs), currentPairs, CIntVector.getCPtr(pseudoknotPairs), pseudoknotPairs);
  }

  public static void findPseudoknots(CIntVector currentPairs) {
    RNABackendJNI.findPseudoknots__SWIG_2(CIntVector.getCPtr(currentPairs), currentPairs);
  }

  public static String getDataPath(String defaultPath) {
    return RNABackendJNI.getDataPath__SWIG_0(defaultPath);
  }

  public static String getDataPath() {
    return RNABackendJNI.getDataPath__SWIG_1();
  }

  public static void setDataPath(String path) {
    RNABackendJNI.setDataPath(path);
  }

}
