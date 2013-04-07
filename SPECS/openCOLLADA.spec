%global SHA 1a78575c07

# Upstream does not maintain a soversion so we define one here.
# abi-compliance-checker will be used to determine if an abi breakage occurs
# and the soversion will be incremented.
%global sover 0.1


Name:           openCOLLADA
Version:        0
Release:        14.git%{SHA}%{?dist}
License:        MIT
Summary:        Collada 3D import and export libraries
Url:            http://www.opencollada.org/
Group:          System Environment/Libraries

# SOURCE URL: https://github.com/KhronosGroup/OpenCOLLADA
# This build uses openCOLLADA git:1a78575c07ebb2bd0f6fe5341a9ab4d6e1db09c9
# $ git clone https://github.com/KhronosGroup/OpenCOLLADA.git
# $ cd OpenCOLLADA
# $ git archive --format=tar.gz --prefix=openCOLLADA-0-14.git1a78575c07/ \
# 1a78575c07ebb2bd0f6fe5341a9ab4d6e1db09c9 -o ../openCOLLADA-0-14.git1a78575c07.tar.gz 

Source0:        %{name}-%{version}-14.git%{SHA}.tar.xz

BuildRequires:  dos2unix
BuildRequires:  fftw-devel
BuildRequires:  pcre-devel
BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel

%description 
COLLADA is a royalty-free XML schema that enables digital asset
exchange within the interactive 3D industry.
OpenCOLLADA is a Google summer of code opensource project providing
libraries for 3D file interchange between applications like blender.
COLLADABaseUtils          Utils used by many of the other projects
COLLADAFramework          Datamodel used to load COLLADA files
COLLADAStreamWriter       Sources (Library to write COLLADA files)
COLLADASaxFrameworkLoader Library that loads COLLADA files in a sax
                          like manner into the framework data model
COLLADAValidator          XML validator for COLLADA files, based on
                          the COLLADASaxFrameworkLoader
GeneratedSaxParser        Library used to load xml files in the way
                          used by COLLADASaxFrameworkLoader

%package        doc
Summary:        Developer documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
This package provides documentation for %{name}.

%package        devel
Summary:        Include files for openCOLLADA development
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the include files necessary to build and
develop with the %{name} export and import libraries.

%package        utils
Summary:        XML validator for COLLADA files
Group:          Development/Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
XML validator for COLLADA files, based on the COLLADASaxFrameworkLoader.


%prep
%setup -q -n %{name}-${release}

# Remove unused bundled libraries
#rm -rf Externals/{Cg,expat,lib3ds,LibXML,MayaDataModel,pcre,zlib,zziplib}

# Add some docs, need to fix eol encoding with dos2unix in some files.
find ./ -name .project -delete
cp -pf COLLADAStreamWriter/README README.COLLADAStreamWriter
cp -pf COLLADAStreamWriter/LICENSE ./

iconv -f ISO_8859-1 -t utf-8 COLLADAStreamWriter/AUTHORS > \
  COLLADAStreamWriter/AUTHORS.tmp
touch -r COLLADAStreamWriter/AUTHORS COLLADAStreamWriter/AUTHORS.tmp
mv COLLADAStreamWriter/AUTHORS.tmp COLLADAStreamWriter/AUTHORS

dos2unix -f -k README.COLLADAStreamWriter
dos2unix -f -k LICENSE
dos2unix -f -k README
find htdocs/ -name *.php -exec dos2unix -f {} \;
find htdocs/ -name *.css -exec dos2unix -f {} \;

# Install Changelog
install -p -m 0644 %{S:1} ./

%build
rm -rf Build && mkdir -p Build && pushd Build
%cmake -DUSE_STATIC=OFF \
       -DUSE_SHARED=ON \
       -Dsoversion=%{sover} \
       -DCMAKE_SKIP_RPATH=ON \
       -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
       ../

make %{?_smp_mflags}


%install
pushd Build
make DESTDIR=%{buildroot} install

# Manually install binary
mkdir -p %{buildroot}%{_bindir}/
install -p -m 0755 bin/* %{buildroot}%{_bindir}/

popd

# Install MathMLSolver headers
mkdir -p %{buildroot}%{_includedir}/MathMLSolver
cp -a Externals/MathMLSolver/include/* %{buildroot}%{_includedir}/MathMLSolver/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README LICENSE README.COLLADAStreamWriter COLLADAStreamWriter/AUTHORS Changelog
%{_libdir}/lib*.so.%{sover}

%files doc
%doc htdocs/

%files devel
%{_libdir}/*.so
%{_includedir}/*

%files utils
%{_bindir}/*


%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-13.svn871
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Richard Shaw <hobbes1069@gmail.com> - 0-12.svn871
- Update to latest svn.
- Add MathMLSolver includes.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 0-11.svn864
- Rebuild against PCRE 8.30

* Thu Jan 05 2012 Richard Shaw <hobbes1069@gmail.com> - 0-10
- Rebuild for GCC 4.7.0.
- Change how library soversion is set and test for abi breakages.
- Fix overriding of required build flags.

* Wed Oct 26 2011 Richard Shaw <hobbes1069@gmail.com> - 0-9
- Update to svn revision 864.

* Wed Oct 26 2011 Richard Shaw <hobbes1069@gmail.com> - 0-8
- Update to svn revision 863.
- Fix typo in spec file.

* Thu Oct 06 2011 Richard Shaw <hobbes1069@gmail.com> - 0-6
- Update to svn revision 847.

* Wed Apr 27 2011 Richard Shaw <hobbes1069@gmail.com> - 0-5
- Created -utils and -doc sub-packages.
- Corrected installation location of -devel header files.

* Wed Apr 27 2011 Richard Shaw <hobbes1069@gmail.com> - 0-4
- Move from scons to cmake for building.
- Various other fixes.

* Thu Apr 21 2011 Richard Shaw <hobbes1069@gmail.com> - 0-3
- Switched from expat to libxml2 for xml support.
- Updated to svn838

* Fri Apr 15 2011 Richard Shaw <hobbes1069@gmail.com> - 0-2
- Updated spec file for better packaging compliance
- Fixed some rpmlint warnings

* Wed Apr 12 2011 Richard Shaw <hobbes1069@gmail.com> - 0-1
- Updated spec file for Fedora packaging compliance

* Thu Mar 31 2011 davejplater@gmail.com
- Update to svn836
- Upstream changes :
  * fix validation preprocessor flag
  * inti member variables
  * fix uri copy ctor, add missing includes
  * replace asserts
  * fix import
  * fix crash in utf conversion with recent gcc
  * replace asserts by custom assert

* Fri Feb 11 2011 davejplater@gmail.com
- Update to svn827
- Upstream changes:
  * fix Issue 125: cgfx shader source file is not honoring the
  search path on export.
  * fix Issue 89: CONTINUITY semantic is not defined. Define all
  semantics in COLLADASWInputList.h
  * partially fix Issue 71: wrong opacity for effects without set
  transparency
  * fix Issue 65: COLLADASaxFWL::Loader::loadDocument() don't check
  if the file correctly loads
  * fix Issue 62: build fixes for linux (gcc 4.4.3)
  * ignore bin and lib folder in pcre
  * Issue 35: IWriter start, cancel, and finish methods not called
  * remove precompiled pcre pattern from source
  * fix Issue 122: Root::loadDocument("../a/b/c.dae") attempts to
  open "../a/a/b/c.dae"
  * Issue 145: std::terminate() while loading lightwave dae through
  OpenCOLLADAValidator
  * fix Issue 146: OpenCOLLADAValidator crash
  COLLADASaxFWL::LibraryEffectsLoader::handleTexture
  * fix Issue 151: CMakeLists.txt overwrites custom CMAKE_CXX_FLAGS
  * Issue 153: crash in <articulated_system> improvements in
  kinematics loader related to mathml

* Fri Jan  7 2011 davejplater@gmail.com
- Spec file change to fix SLE_11_SP1 build made by repabuild.

* Mon Dec 27 2010 davejplater@gmail.com
- Update to svn788
- Upstream changes
  * fix Issue 148: Glitch in ftoa and dtoa (rename variables)

* Mon Nov 22 2010 davejplater@gmail.com
- Update to svn785
- Prevent build of dae2ogre with openCOLLADA-nodae2ogre.patch
- Upstream changes :
  * apply path from Issue 4: CMake or Scons
  * fix performance issue with many materials
  * fix: do not write empty <extra> element in <profile_COMMON>
  * apply patch (only first change) provided in Issue 136: Fix for
  color sets not exporting in colladaMaya
  * fix Issue 137: SetParam does not properly export float<n> with
  0's in it

* Sat Nov  6 2010 davejplater@gmail.com
- Update to svn 779 Removed openCOLLADA-assign_value.patch which is
  already incorporated in this revision.
- Upstream changes :
  * fix Issue 126: cgfx shader source file is not honoring the search
  path on export.
  * apply patch provided in Issue 4: CMake or Scons (add cmake files)
  * fix Issue 132: Small fix from compiling blender - collada with
  - Wall -Werror
  * fix Issue 131: Gcc will be initialized after warning fixes

* Tue Oct 26 2010 pth@suse.de
- Actually assign the passed value in setter function.
- Manually strip libraries

* Sun Oct 24 2010 davejplater@gmail.com
- Added patch COLLADA-linuxbuild.patch to fix shared lib build includes.
- Added patch openCOLLADA-buildflags.patch for optflags.
- Added patch openCOLLADA-soname.patch to add sonames to libs.

* Mon Oct 18 2010 davejplater@gmail.com
- Created new package openCOLLADA needed by blender-2.5x
- OpenCOLLADA is a stream based reader and writer library for
  COLLADA files. support@opencollada.org
