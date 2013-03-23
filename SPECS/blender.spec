#
# spec file for package blender
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define collada 1
%define wplayer 1
%define documentation 0

# Use rpmbuild -D 'DISTRIBUTABLE 0' to build original code.
%define DISTRIBUTABLE 0

Name:           blender
Version:        2.66a
Release:        1.1
%define _version 2.66a
Summary:        A 3D Modelling And Rendering Package
License:        GPL-2.0+
Group:          Productivity/Graphics/3D Editors
Url:            http://www.blender.org/

Source0:        http://download.blender.org/source/%{name}-%{version}.tar.gz

BuildRequires:  gettext-tools
%if 0%{?suse_version} > 1210
BuildRequires:  libGLw-devel
%else
BuildRequires:  MesaGLw-devel
%endif
BuildRequires:  libexpat-devel
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11
%if %documentation == 1
Recommends:     blender-doc
%endif
# libquicktime-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  SDL-devel
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  epydoc
BuildRequires:  fdupes
BuildRequires:  fftw3-devel
BuildRequires:  gcc-c++
BuildRequires:  glew-devel
BuildRequires:  graphviz
BuildRequires:  help2man
BuildRequires:  hicolor-icon-theme
BuildRequires:  jack-audio-connection-kit-devel
#BuildRequires:  libao-devel
BuildRequires:  libdrm-devel
BuildRequires:  libjpeg8-devel
BuildRequires:  liblcms-devel
BuildRequires:  libpng-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libtiff-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  lzo-devel
BuildRequires:  openal-soft-devel
BuildRequires:  openssl-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  perl-Text-Iconv
#BuildRequires:  ruby
#BuildRequires:  ruby-devel
BuildRequires:  shared-mime-info
BuildRequires:  xorg-x11-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  yasm
BuildRequires:  yasm-devel
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libxml-2.0)
%if 0%{?collada} == 1
BuildRequires:  openCOLLADA-devel
%endif
BuildRequires:  graphviz
BuildRequires:  liblcms-devel
BuildRequires: OpenColorIO-devel
BuildRequires: OpenImageIO-devel
BuildRequires: llvm-devel
BuildRequires: libffmpeg-devel
# See bnc#713346
Requires:       python3-xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Blender is a 3D modelling and rendering package. It is the in-house
software of a high quality animation studio, Blender has proven to
be an extremely fast and versatile design instrument. The software
has a personal touch, offering a unique approach to the world of
Three Dimensions. Use Blender to create TV commercials, to make
technical visualizations, business graphics, to do some morphing,
or design user interfaces. You can easy build and manage complex
environments. The renderer is versatile and extremely fast. All
basic animation principles (curves & keys) are well implemented.It
includes tools for modeling, sculpting, texturing (painting,
node-based shader materials, or UV mapped), UV mapping, rigging and
constraints, weight painting, particle systems, simulation (fluids,
physics, and soft body dynamics and an external crowd simulator),
rendering, node-based compositing, and non linear video editing,
as well as an integrated game engine for real-time interactive 3D
and game creation and playback with cross-platform compatibility.

%if %documentation == 1
%package doc
Summary:        Documentation for blender
Group:          Documentation
BuildArch:      noarch

%description doc
Being the in-house software of a high quality animation studio, Blender
has proven to be an extremely fast and versatile design instrument. The
software has a personal touch, offering a unique approach to the world
of Three Dimensions. Use Blender to create TV commercials, to make
technical visualizations, business graphics, to do some morphing, or
design user interfaces.
This package includes API documentation and example plugin programs.
%endif

%lang_package

%prep

%setup -q
#%patch0 -p1

%if %DISTRIBUTABLE == 1
rm -rf release/scripts/presets/ffmpeg
%endif

# binreloc is not a part of fedora
#rm -rf extern/ffmpeg
#rm -rf extern/fftw
#rm -rf extern/glew
#rm -rf extern/libmp3lame
#rm -rf extern/libopenjpeg
#rm -rf extern/libredcode
#rm -rf extern/ode
#rm -rf extern/x264
#rm -rf extern/xvidcore
#rm -rf extern/qhull
#rm -rf extern/make
#rm -rf extern/verse

%build
__libsuffix=$(echo %_lib | cut -b4-)
mkdir -p Build && pushd Build
cmake ../ -DBUILD_SHARED_LIBS:BOOL=OFF \
      -DWITH_FFTW3:BOOL=ON \
      -DWITH_JACK:BOOL=ON \
      -DWITH_CODEC_SNDFILE:BOOL=ON \
      -DWITH_CODEC_FFMPEG:BOOL=ON \
      -DWITH_IMAGE_OPENJPEG:BOOL=ON \
      -DWITH_OPENCOLLADA:BOOL=ON \
      -DWITH_PYTHON:BOOL=ON \
      -DWITH_PYTHON_INSTALL:BOOL=ON \
      -DWITH_GAMEENGINE:BOOL=ON \
      -DWITH_OPENCOLORIO:BOOL=ON \
      -DOPENCOLORIO_INCLUDE_DIR:PATH=/usr/include/OpenColorIO \
      -DWITH_CYCLES:BOOL=ON \
      -DWITH_OPENIMAGEIO:BOOL=ON \
      -DOPENIMAGEIO_ROOT_DIR:PATH=/usr \
%if %wplayer == 1
      -DWITH_PLAYER:BOOL=ON \
%else
      -DWITH_PLAYER:BOOL=OFF \
%endif
      -DWITH_INSTALL_PORTABLE:BOOL=OFF \
      -DWITH_MOD_OCEANSIM:BOOL=ON \
      -DWITH_LLVM:BOOL=ON \
%if 0%{?suse_version} > 1220 || 0%{?sles_version}
      -DPYTHON_VERSION=3.3 \
      -DPYTHON_LIBPATH=/usr/lib"$__libsuffix" \
      -DPYTHON_LIBRARY=python3.3m \
      -DPYTHON_INCLUDE_DIRS=/usr/include/python3.3m \
%endif
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}

make %{?_smp_mflags}
popd

%if %documentation == 1
# Build documentation
pushd doc/doxygen
doxygen -u Doxyfile
doxygen Doxyfile
popd
mv doc/doxygen/html doc/
rm -rf doc/doxygen
%endif	# documentation

%install
export blender_version=$(grep BLENDER_VERSION source/blender/blenkernel/BKE_blender.h | tr -dc 0-9)
export blender_version=$(expr $blender_version / 100).$(expr $blender_version % 100)
%define rlversion %(echo $blender_version)
echo "release version = $blender_version"
echo "rlversion is %{?rlversion}"

# make install
pushd Build
%make_install
popd

# Remove folder, it's not supposed to be installed here.
# rm -rf %{buildroot}%{_datadir}/%{name}/%{_version}/datafiles/fonts

# Factory is now of the opinion that every /usr/bin file needs a man page,
%if %wplayer == 1
# Generate man page with help2man
pushd %{buildroot}%{_mandir}/man1
cp -v %{buildroot}%{_bindir}/blenderplayer ./
help2man \
	--version-string="%{version}" \
	--help-option="-h" -n "a utility for previewing .blend files" \
	-s 1 -m "User Commands" -S "Stichting Blender Foundation" -N -o blenderplayer.1 ./'blenderplayer -h ""'
rm blenderplayer
popd
%endif	# wplayer == 1

%if 1 == 0
# Fix any .py files with shebangs and wrong permissions.
if test -z `find %{buildroot} -name *.py -perm 0644 -print0|xargs -0r grep -l '#!'`; \
then break;
else chmod -f 0755 `find %{buildroot} -name *.py -perm 0644 -print0|xargs -0r grep -l '#!'`; \
fi

# Copy text files to correct place.
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -v    %{buildroot}%{_datadir}/doc/blender/* %{buildroot}%{_docdir}/%{name}/
rm -rf %{buildroot}%{_datadir}/doc/blender
%endif	# 1 == 0

%if 0%{?sles_version}
%suse_update_desktop_file -i -n -G "Blender Template" x-blend
%suse_update_desktop_file -i -n blender
%else

# Validate blender.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/blender.desktop
%endif

#%fdupes %{buildroot}%{_datadir}/%{name}/%{rlversion}/scripts/

#%find_lang %{name} %{?no_lang_C}

%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
#touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    # touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

#%posttrans # I don't find this keyword in RPM Guide
#gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

#%files lang -f %{name}.lang

%files
%defattr (-, root, root)
%{_prefix}/*

%if %documentation == 1
%doc %{_docdir}/%{name}

%files doc
%defattr (-, root, root)
%doc doc/
%endif	# documentation

%changelog
* Fri Mar 21 2013 zhanggyb@gmail.com
- Simplify this spec, remove all patches and extra sources
- Update to version 2.66a
- add OpenImageIO, OpenColorIO support

* Mon Nov  5 2012 Rene.vanPaassen@gmail.com
- need buildroot for SLED
- need to define PYTHON_LIBPATH etc for SLED also
- modified desktop file installation for SLED
* Thu Nov  1 2012 dvaleev@suse.com
- fix big endian build (blender-2.64a-big-endian.patch)
* Mon Oct 29 2012 p.drouand@gmail.com
- Update to version 2.64a:
  + See
    http://www.blender.org/development/release-logs/blender-263/
    for upstream changes.
- Update fix-locale-files-path patch for 2.64 version
- Remove unneeded fedora conditional macros
- Add python3 version option on configure cmake
- Add a patch to correct python development files on Factory
- Fix build for Factory
* Fri Sep 21 2012 idonmez@suse.com
- Add explicit glu dependency
* Mon Jul 30 2012 coolo@suse.com
- just use default libjpeg on opensuse
* Thu Jun 21 2012 Rene.vanPaassen@gmail.com
- Need a BuildRoot: defined, for building on SLE 11
* Fri May 11 2012 badshah400@gmail.com
- Update to version 2.63a:
  + See
    http://www.blender.org/development/release-logs/blender-263/
    for upstream changes.
- Add blender-fix-locale-files-path.patch to fix the path where
  locale files are installed. Split out a lang package with extra
  locale files.
- Do not enable verbose make file logs.
* Thu May  3 2012 davejplater@gmail.com
- Used Fedora 2.62 src rpm packaged by Richard Shaw to update to
  version 2.63
- Patch blender-2.62-blenkernel.patch no longer needed upstream
  remove all undistributable directories if ffmpeg is disabled or
  not available.
- blender-collada858.patch no longer needed, fixed upstream
- blender-gcc47.patch no longer needed, fixed upstream
- Blender now fully compatible with "second life" see bnc#652536
- See http://www.blender.org/development/release-logs/blender-263/
  for upstream changes.
* Wed Apr 11 2012 dimstar@opensuse.org
- Add blender-collada858.patch: openCOLLADA >= svn 858 installs
  the headers to /usr/include/COLLADA* instead of
  /usr/include/COLLADA*/include, thus messing up the build of
  blender.
- Add blender-gcc47.patch: Fix build with gcc 4.7. Taken from
  upstream svn, r44000.
* Wed Sep  7 2011 davejplater@gmail.com
- Update to release 2.59, added patch
  blender-2.59-colladainclude.patch to correct build.
- Upstream changes:
  * This is mostly a bug fix release with 140 fixes since 2.58a.
  Additions include improved keymap editing, 3D mouse support,
  some new addons and Node UI improvements.
  too numerous to list all please refer to:
  http://wiki.blender.org/index.php/Dev:Ref/Release_Notes/changelog_259
* Tue Sep  6 2011 davejplater@gmail.com
- Added "Requires: python3-xml to fix bnc#713346
* Wed May  4 2011 davejplater@gmail.com
- Created blender-2.57b-nobuffer_ftoa_utf_link.patch to stop
  blender's linker looking for libs buffer, ftoa and UTF from
  openCOLLADA as these libs are now static included in the other
  libraries and no longer exist.
* Thu Apr 28 2011 davejplater@gmail.com
- Update to blender-2.57b Release.
- Fix new patch blender-2.56-gcc46.patch to apply cleanly.
- Upstream changes :
  * The Blender Foundation and online developer community is proud to
  present Blender 2.57a. This is the first stable release of the
  Blender 2.5 series, representing the culmination of many years of
  redesign and development work.
  * We name this version "Stable" not only because it's mostly feature
  complete, but especially thanks to the 1000s of fixes and feature
  updates we did since the 2.5 beta versions were published.
  * The next 2 months we will keep working on finishing a couple of
  left-over 2.5 targets and we expect to get feedback and bug reports
  from users to handle as well. If all goes well, the 2.58 version
  then can be the final release of the 2.5 series, with a massive
  amount of new projects to be added for an exciting cycle of 2.6x
  versions. Target is to release updates every 2 months this year.
* Thu Apr 28 2011 idoenmez@novell.com
- Add blender-2.56-gcc46.patch to fix compilation with gcc 4.6
* Sun Apr 17 2011 davejplater@gmail.com
- Update to blender-2.57 stable
- Upstream news :
  The Blender Foundation and online developer community is proud to
  present Blender 2.57. This is the first stable release of the
  Blender 2.5 series, representing the culmination of many years of
  redesign and development work.
  We name this version "Stable" not only because it's mostly feature
  complete, but especially thanks to the 1000s of fixes and feature
  updates we did since the 2.5 beta versions were published.
  The next 2 months we will keep working on finishing a couple of
  left-over 2.5 targets and we expect to get feedback and bug reports
  from users to handle as well. If all goes well, the 2.58 version
  then can be the final release of the 2.5 series, with a massive
  amount of new projects to be added for an exciting cycle of
  2.6x versions. Target is to release updates every 2 months this year.
* Thu Apr 14 2011 davejplater@gmail.com
- Update to blender-2.57.36147 2.57 release.
- For upstream changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Thu Apr  7 2011 davejplater@gmail.com
- Update to blender-2.57.36007
- For upstream changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Mon Apr  4 2011 davejplater@gmail.com
- Update to blender-2.57.35927
- For upstream changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Wed Mar 23 2011 davejplater@gmail.com
- Update to blender-2.56.35927
- For upstream changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Tue Mar 22 2011 davejplater@gmail.com
- Update to blender-2.56.35701
- For upstream changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Tue Mar  8 2011 davejplater@gmail.com
- Update to blender-2.56.35402
- Enable blenderplayer to build
- For more changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Mon Mar  7 2011 davejplater@gmail.com
- Update to blender-2.56.35390
- Upstream changes :
  * fix for building with opencollada 833 on linux.
  For more changes see :
  /usr/share/doc/packages/blender/Changes.txt
* Thu Feb 17 2011 davejplater@gmail.com
- Update to blender-2.56.34784
- For upstream changes see /usr/share/doc/packages/blender/Changes.txt
* Sat Feb 12 2011 davejplater@gmail.com
- Update to 2.56 beta svn snapshot blender-2.56.34
- Upstream changes:
- *Bugfixes: #26021, #26039, #26040, #25973, #25978, #26030
  [#26013], #26001, #26004, #26002, #26007, #25831, #25968, #25523,
  [#25969], #25957, #25977, #25975, #25693, #25801, #25970, #25965,
  [#25963], #25926, #25955, #25934, #25951, #25953, #25937, #25824,
  [#25947], #25948, #25693, #25944, #25608, #25871, #25923, #25933
  * For many new features and 2.49 functionality restored see :
  /usr/share/doc/packages/blender/Changes.txt
* Sat Jan  1 2011 davejplater@gmail.com
- Update to 2.56 beta svn snapshot blender-2.56.34000
- Upstream changes :
  The Blender Foundation and online developer community is proud to
  present Blender 2.56 Beta. This release is the fourth official
  beta release of the Blender 2.5 series, representing the
  culmination of many years of redesign and development work.
  This version is called a "Beta" because it's now for the most
  part feature complete. The Python API has had some extensive
  changes, most notably in naming conventions and in creation and
  access of properties.
  Since Blender 2.55 beta over 440 bugs were fixed!
* Tue Dec 14 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33653
- Upstream bugfixes :
  [#25211], #25209, #23922, #23826, #25207, #23420, #25191, #25197,
  [#25199], #25178, #25184, #25185, #25188, #24752, #23395, #25186,
  [#25183], #25179, #25177, #22967, #25071, #22477, #25106, #25170,
  [#25153], #25095, #25135, #25116, #25155, #25154, #25159, #25027,
  [#25150], #25147, #25120, #25119, #25104, #24814, #20598, #25099,
  [#25086]
- Upstream changes :
  * New math util funcitons:
  equals_v2v2
  project_v2_v2v2
  isect_seg_seg_v2_point
  which would be necessery for my further multires interpolation
  commit
  * M_Geometry_LineIntersect2D now uses isect_seg_seg_v2_point().
  * Behaviour of this function was changed a bit -- it haven't
  returned intersection point in several cases when two segments
  are making angle.
  * 2.4 feature back:
  For constraints that have 'disabled' flag (because it has
  invalid input) the name was drawn in red. Easy to recognize
  constraints that stopped working.
  * Moved extensions_framework into addons/modules
* Wed Dec  8 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33554
- Upstream changes :
  * Bugfixes #25023 #25003 #25060 #21246 #25073 #25076 #25074
  [#25049] #24163a #25085 #25079 #25088 #25081 #25082 #24052
* Mon Dec  6 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33504
- Upstream changes :
  * CMake: use a global list to store libraries built rather then
  cmake_blender_libs.txt file
  * bugfixes [#24967] [#24995] [#25057] [#25030] [#25046] [#25047]
  [#22663] [#25050] [#25041] [#25042] [#25036]
  * Fixed memory leak in thumbnail_joblist_free
  * fix for camera border going outside the clipping range while in
  camera view.
  * use constant strings for outliner menus rather then sprint'ing
  them together.
  * Fixed dead-lock when subviding curve
  * use PyUnicode_DecodeFSDefault rather then
  PyUnicode_DecodeUTF8(str, strlen(str), "surrogateescape"),
  for converting non utf8 names.
  * extensions_framework: prefer user config and scripts dirs, if
  set, to save addon config files to.
  * Dependency graph: changed DAG_id_flush_update to
  DAG_id_tag_update.
  * bpath iterator updates
  * use BLI_strnlen rather then strlen when comparing against fixed
  lengths.
* Sat Dec  4 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33472
- Upstream changes :
  * Bug fix #21900, Bugfix #21893, Bugfix #24699, Bugfix #25033
  * Give functions that use printf style formatting GCC format attributes
  so if incorrect formatting is used the compiler will warn of this.
  * minor changes to bone UI script.fix for strict prototype error.
  * remove shadowed definitions but keep them as zero this time.
  * Const conflict in PIL_dynlib_find_symbol
  * Bugfix #2508, Bugfix #24568, Bugfix #25026, Bugfix #24999
  * Curve editmode was missing hotkey for operator "Select Inverse"
  Is now added like Mesh, CTRL+I
  * Text editor, "Add new" caused zero-user block.
  * Nurbs edit: 'switch order' crashed when order was higher than amount of
    points.
  * Fix for compilation error caused by strict prototype checking
  * Fix #25017: Bezier Curve Deform Twisting after adding Shape Keys
  * Bugfix #20565, Bugfix #24890, Bugfix #24903, Bugfix #25010
  * Fix for [#24899]Align Objects operator was broken due to incorrect order of vector by
  matrix multiplication
  * updates to patch from Dan Eicher, allow adding a NodeGroup through bpy.data.node_groups.new(name, type)
  * fix [#24938] Seed value on Particle settings gives Error when trying to insert key.
  * fix [#25015] Ctrl+L linking to scene list does not scroll when the list is larger than screen resolution
  correction to error message from Dan Eicher
  * fix crash when report timer was set but no usable error reports were found.
  * Fix for [#25006] Particle system crash (missing check for negative index)
  * bugfix [#24913] Text bevel normals wrong
  * Fix for [#25001] Enable Smoke High Resolution is greyout after baking
  * Additional fix for #24958 Cloth pinning not working
  * Adding some descriptions for animation-related operators that were missing them.
  * patch [#23212] Python api for Nodes
  * fixed crash with rigid body constraints not having their child pointer read correctly.
  * Fix for [#24958] Cloth pinning not working
* Wed Dec  1 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33410
- Upstream changes :
  * fix for crashes trying to resolve paths "location[]" or "location.."
  * increase the reference counts when setting default scene compo nodes
  else removing them can set the user count < 0.
  * quit blender if the first X11 window fails to open.
  mainly just to avoid a segfault so the user knows its not a bug.
  * workaround [#24958] Cloth pinning not working
  * bugfix [#23406] DPX Images load darker then saved, UI broken.
  * patch from JacobF on IRC, copy smoke settings. double checked none
  of these are used for runtime.
  * bugfix [#22638] Alpha channel not saved when using texture paint
  * minor console changes.
  remove report argument from console functions.
  don't update the scroll area while drawing, do this within operators instead.
  dont redraw while selecting text unless selection changes.
  * bugfix [#23423] Multi-window : closing game windows cause blender crash
  * Smoke now uses only one point cache where both normal and high resolution smoke are stored together:
    Separate caches were causing quite a lot of problems both in principle and practice.
    For example it doesn't really make sense to have different frame ranges for normal and high resolution smoke, but this was fully possible before.
    Also to fully bake the smoke you had to do a "Bake All Dynamics", which completely defeats the whole point of the feature!
    As a result of this change the smoke cache usage is much much simpler and less error prone.
    This is quite a big change, but hopefully there should be less rather than more problems as a result :)
  Some other related changes:
    Changing the cache name now works for disk caches properly too, it
    now just renames the cache files so should be faster too!
    Smoke is now always forced to disk cache with step 1 on file load
    as there were some strange cases where smoke was trying to use memory cache.
    Disabled smoke debug prints from console.
    Disabled changing smoke parameters when smoke is baked.
  * misc small changes.
    commented unused View3D->flag's
    popup dialog now centers over the mouse
    only overwrite image alpha with render settings on save if saving the render result.
  * Bugfix #24986 bugfix [#24974] bugfix [#24798] Bugfix #24976 fix [#24990]
* Mon Nov 29 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33375
- Upstream changes :
  * fix for error when changing DISBALE_PYTHON -> WITH_PYTHON,
  * Fix [#24964] HISTOGRAM: Inconsistency in spaces
  * Fix [#20241] half-transparent objects in volume have no shadow.
  * include headers in cmake source, added a script to check for
  consistency, reporting missing headers & C files.
  * Fix: [#24170] Camera inside volume error, [#24838] Light inside
  Volume material drops on it's walls - it may be double
  * fix [#24921] Crash after inserting keyframing UV coords and
  changing frame in edit mode zero length arrays were still having
  their members accessible.
  * bugfix [#24947] Animations data replaced by the first animation (fbx exporter)
  * Bugfix #24933
  * Bugfix #24953
  * bugfix "Export UV Layout" stalls when saving file in 2.55b
  * fix for fix [#24955] Generating UV-Images within blender (Alt-N) not possible
  * Detect Gallium driver. Extend NPoT workaround to opensource drivers.
  * Bugfix #21385
  * [#24935] Proportional translation size stuck to none
  * bugfix [#24944] Crash on attempting to keyframe HSV color prevent eternal loop
  * console text underscore would draw outside the view for larger font sizes.
  * fix for fix r33330, bug [#23118].
  * Particle draw was calling glColorMaterial(...) after glEnable(GL_COLOR_MATERIAL),
  * added option to turn off Text anti-aliasing in the UI
  * Fix #24914: 3D text glitch and crash
  * remove support for rna resolving paths with collection['name'],
  only support collection["name"],
  * Rigid Body Joint Constraint:
  * Update nurb keyindex data when subdividing
  * fix building blenderplayer and a divide by zero bug with the console view.
  * "Fix" for [#24934] Particle single user crash
  * Bug fix: voxeldata texture extension didn't work.
  * lasso select wasn't comparing the depth with particle selection, where border and circle select do.
  * bugfix [#23118] Blender freezes when combing hair - OS X path changes related?
  * freeing all free GPU buffers every frame could be a performance issue and is not necessary
* Fri Nov 26 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33326
- Upstream fixes :
  * follow up of "Bugfix #23576" (Logic UI)
  * Fix #24855: disabling shadows didn't disable AO/env with ray transparency
  and AO multiply mode.
  * BGE Bugfix: [#24926]
  * Fix #24923: tweak falloff strength tooltip to apply both to AO and indirect.
  * Fix #24775: boolean modifier crash in rendering on Mac. Problem was that this
  ran out of stack memory, now it passes some arguments by reference instead of
  by value to use less stack space.
  * ATI X1xxx gfx cards (R500 chipset) lack full support for npot textures
  although they report the GLEW_ARB_texture_non_power_of_two extension.
  * Smoke domain resolutions were calculated wrong for non-cube domains in some cases.
  * bugfix while looking into [#24900], color wasn't being set for face-mask mode.
  * bone roll recalculate, option to use active bones Z axis.
  * bugfix [#24907] bone roll z up broken and python script showing correct
  method to roll bones
  * Fixed bug with Text menu in font edit mode
  * fix for https://projects.blender.org/tracker/index.php?func=detail&aid=24442&group_id=9&atid=498
  * [#24442] GLSL + VBOs
  * bugfix [#24916] Blender Crash after inappropriate Merge-Command
  * Redraw 3d view when new object was added (NC_OBJECT|NA_ADDED notifier)
  This fixes one issue from #24914: 3D text glitch and crash ("delayed" 3d view refresh)
  * Possible fix for the issue that came up in [#24890] Vector Blur node is Buggy
  * Fix polling order for ui panels in netrender.
  * Spline IK Bugfix:
  * drivers could reference invalid index values outside the bounds of the array.
  * define UNUSED() locally for mmap_win
  * fix for crash introduced r33257, also tag some vars as unused.
  * fix [#24893] Minor error message glitch
  * bugfix [#24884] Loading any preset leads to crash
  * bugfix [#24887] Crash on snapping verts on other object
  * close addon files, Py3.2 now complains when files are left open.
  * Bugfix #24887
  * fix for crash canceling fly mode.
  * Bugfix #24847
  * add a window manager to files loaded from 2.4x in background mode.
  (partial fix for [#24882]).
  * Bugfix #23576
  * Fix #24782: proxy armature Layer state not saved with file. Was in 2.4x but
  not ported to 2.5x, implemented a bit different now to fit RNA better.
  * fix [#24879] "Feather" symmetry option in sculpt mode crashes.
  * rotate_m4() was being called with axis=0
  * Fix for [#24877] Cloth + hair bug
  Particles needed the original index layer, but didn't ask for it.
  * Fixes for [#24862] Fluid Simulator issues
  * bugfix [#23871] OSX panel button bug (Python Namespace issue)
  * Remove library specification.
* Wed Nov 24 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33275
- Upstream changes :
  * When exporting images also add the string name (attribute). This
  is optional, but it helps other viewers importing from Blender
    .dae exports.
  * Fix #24834: curves extrude + bevel gave bad normals on rendering.
  * Small feature fix: zero-user blocks get indicated with "0" again
  in browsing.
  * Previous commit cleaned up one variable too many, breaking
  adding torus/tube in Nurbs editmode.
  * Bugfix #24860
  * use unit system for the grid floor (was only ortho before).
  * minor edits to exception formatting (remove . or \n from suffix)
  * bugfix [#24871] Unwrapping with Smart Project give a bad result.
  * fix for typo in mathutils vec.to_track_quat() argument parsing.
  * Changed some ui names for smoke parameters to make things less
  ambiguous.
  * Fix for [#19706] Smoke 'sticks' to Collision objects initial
  position
  * Changes to the ortho grid drawing based on discussion with Ton.
  * Cached smoke wasn't being drawn on file load before going to
  simulation start frame.
  * transform snapping to a unit scaled grid was broken.
  * fix [#24870] ObjectActuator.offset_rotation in radians
  * partial fix for [#23532]
  * Particle fluid and boid settings didn't have a valid rna path,
  so they couldn't be animated.
  * use zero initializers instead of memset(), also change
  PointerRNA_NULL from an extern into a define.
* Tue Nov 23 2010 davejplater@gmail.com
- Update to svn snapshot blender-2.55.33249
- Upstream changes :
  * extensions_framework: fix UI  drawing logic
  * Partial fix for #24773: Material Nodes - there isn't able to set keys on Mapping coordinates
  * Playback now works.
  * fix for player with recent update.
  * fix for cmake if build flags are not defined.
  * Fix #24596: specular toggle on material didn't work correct.
  * fix [#24866] object/transform/align objects error
  * bugfix [#23609] Lamp PointerProperty, Bugfix #24823
  * More button alignment stuff: campbell had a script that was
  drawing various cases. Fixed another one.
  * Bugfix #24856; bugfix [#24805] bpy operator runs in wrong order or is ignored at all
  * fix for triangulate OBJ export option. reworked fix from Radu Danciu
  * bugfix [#20768] Project Snap Broken rna invoke function wm.invoke_confirm() for python access.
  * find filepaths operator had blend file and search path swapped.
  * blend_m3_m3m3 and blend_m4_m4m4 now support matrices with negative scales.
  * python/mathutils api matrix.lerp(other, factor)
  * new function mat3_to_rot_size(), like mat4_to_loc_rot_size but with no location.
  * fix for fix r33219, reports. Set a valid WM after running UNDO.
  * [#24849] changing objects to another layer causes segmentation fault
  * [#24848] Using an operator outside of edit mode crashes blender
  * [#24844] Crash related to the subdivision (aka subsurf) modifier
  * [#24843] ctrl+z crashes blender
  * rename hide_tooltips_python to show_ ..., tag unused variable with recent sequencer commits.
  * User preference to hide Python references in Tooltips.
  * Fix: 8bit raw and 'blender voxel' voxel data texture formats didn't support relative paths
  * documented and rewrote the render interface of the sequencer.
  * Toggle cyclic on when creating segment between first and last points of non-cyclic bezier
  * Recalc handles after toggling bezier's cyclic flag when deleting segment
  * Applying patch #24822: Select linked for curves as for meshes, CTRL + L version
  * Bugfix #22611, [#22854] Objects lag behind mouse pointer when transformed (translated)
  * [#24652] Project vertices button showing in object mode and leads to wrong behavior.
  * Bugfix #24837, Bugfix #24825. disallow disabling WITH_SAMPLERATE if any audio outputs are enabled.
  * WITH_SAMPLERATE option for cmake.
  * Fixed missed selection oulines for curves/surfaces/fonts/armature when texture shading is active
  * patch from Mike S to enable OpenMP and xcode
  * Bugfix #24824. some more rna range corrections
  * correct exception messages for mathutils constructors.
  * incorrect argument parsing for python opengl module bgl.
  * unsigned byte/short/int were being passes as signed values which would
  * raise an overflow error if a range greater then the signed value was used.
  * fix for RNA ranges exceeding the range of the type.
  * [#24827] Crash when auto-keyframing while playing animation. Bugfix #24792
  * Fixed bug #20620, "VertColors and Flat/Soft imported from 2.49 are wrong
  * Bugfix #21028. Bugfix #24801. Bugfix for [#24768] 6DoF Constraint options missing.
* Tue Nov 16 2010 davejplater@gmail.com
- Update to 2.55.33093
  * Fix [#24310] With high poly numbers when sculpting, modifier keys hang
  reported by Eclectiel L
  When working with very heavy scenes Blender can seem to 'hang' (not responding). Key events that happen
  during this period may get lost, especially for modifier keys.
  Adding extra handling to account for these situations.
  * bugfix [#24696] Export OBJ - Selection Only toggle button has the wrong default state.
  Added convenience function to operators, 'as_keywords()', so operator settings can be passed directly to a function as keyword arguments.
  The problem in this case was that dictionary access to operator properties was not returning rna-property defaults, so as_keywords() ensures all defaults are set.
  * Bugfix, reported in IRC
  The enum "rotmode" was read using an array, without checking for boundary
  cases, causing crashes on bad input. (Wahooney report 2, thanks!)
  * Bugfix #24726
  Doing F1-load a lot of times on same .blend could crash.
  Janne karhu provided a potential fix, which is good to add
  anyway. Will ask him to verify too.
  Added XXX warning for these lines, after filesel exec no
  context variables should be re-used. Is for later investigation.
  * fix for fix, r33086.
  - incorrect range check broke ZYX euler rotations, use MIN/MAX constants so this doesn't happen again.
  - BGE Armature PyAPI also wasn't using correct min/max with rotation modes.
  - clamp on file read rather then when calling the rotation functions, so developers don't use invalid args without realizing it.
  - added assert() checks for debug builds so invalid axis constants don't slip through.
  * patch #24737] PyCObject depreciated in py3k [patch]
  from Dan Eicher (dna), use PyCapsule rather then PyCObject
  * patch [#24742] materials.pop() doesn't decrement user count
  * from Dan Eicher (dna)
  * fix for matrix * vector rotation order.
  * FBX Export, small changes made while looking into reported bug. (no functional changes)
  - Warn for armature deformed meshes which are scaled, these don't work quite the same as in blender, reported as [#24663].
  - Use matrix.decompose() to convert a matrix to loc/rot/scale.
  - get vert/edge/face lists for each mesh only once.
  - faster euler rad -> deg conversion function.
* Mon Nov 15 2010 davejplater@gmail.com
- Update to svn version 2.55.33084
- Upstream changes :
  * bugfix [#24660] (vector * matrix) fails, (matrix * vector) succeeds
  * bugfix [#24665] mathutils.Matrix initialization is counter-intuitive and generates bugs
  was printing transposed, also nicer printing.
  * Getting BLF to work with the Blenderplayer.
  * take delta's into account when applying the objects matrix (dloc, drot, dsize).
  * Now object_apply_mat4() can be used as the reverse of object_to_mat4().
  * add back red tint for zero user datablocks.
  * bugfix [#24682] Render artifacts with mat node
  * Related to #24653: added scene.collada_export() function, to use instead of an
  * operator for external render engines, since operators should not be called in
  * the render() callback.
  * Hide "active" checkbox in ui for "fluid" type fluid objects as it's not used by fluidsim.
  * * Response to report [#24670] Keyframe fluid on/off does not work
  * Bugfix #24335
  * bugfix [#24661] Object.find_armature() only works on meshes
  * Makefile fix for compiling with quicktime.
  * Bugfix #20382
  * Fix for [#24654] Sound Actuator doesn't find the file when Blender is reopened.
  * Patch [#21942] Node links access by Andrey Izrantsev (bdancer) Thanks!
  * update for mathutils vector/matrix order change.
  * fix for own error in recent commit. add a back NULL terminator to the string in text_font_draw_character.
  * fix for own recent error, [#24695] column_vector_multiplication call writes past end of array
  * was setting the vector array out of bounds with vec*=matrix, where the vector wasnt size 4.
  * bugfix [#24702] 3Dmanipulator does not display if view's layers are not synchronize to scene's layers.
  * bugfix [#24697] Trying to run bpy.ops.transform.create_orientation crashes Blender
  * bugfix [#24668] Deleting armature objects removes a user from its action, eventually leading to data loss
  * == filebrowser ==
  * * drawing code cleanup.
  * * list drawing code now uses uiStyleFontDraw like buttons etc.
  * * removed now unused function file_string_width_shortened.
  * * compile fix on non-Windows platforms.
  * [#24639] Snap to Face (retopo) doesn't work when clipping is enabled in mirror modifier.
  * bugfix [#24697]
  * Correct description for Projection property (it doesn't just work on vertice)
  * Seamless texture used for beveled curve is now really seamless (thanks to Mario G. Kishalmi aka lmg)
  * r33039 added dependency to COLLADA for blenderplayer, but it's really not needed there.
  * Stubbing for now.
  * netrender
  * unreported fixes for 3ds import
  * - non ASCII names would break loading.
  * - meshes with no faces would break loading too.
* Tue Nov  9 2010 davejplater@gmail.com
- Update to version 2.55.32968
- Some upstream changes :
  * Bugfix #20812 (and probably others)
  * Bug fix: cutting a sequencer movie strip with sound could crash in some cases.
  * Fix for [#24580] and [#24600]
  * Particles didn't want to stay cached, even if there were no actual chages.
  * Particle states weren't set properly for times before actual simulation start.
  * bugfix [#24403] Object.copy() duplicates armature action
  * bugfix [#24623] VSE strip animation data out of sync after moving using shift-s
  * bugfix [#24578] crash on browse directory w/ broken image file
  * [#24602] Netrender master node IP information is reset to [Default] no matter what
  * [#24601] Net rendering master node fails to send/retrieve files to/from slaves
  * bugfix [#22794] Inconsistent behaviour with Panorama, border rendering
  * fix for last commit with collada
  * bugfix [#24616] Apply Visual Transform doesn't always apply location
  * - object updates were not being flushed, so children weren't updating.
  * - apply the matrix relative to the parent, added this as an option to
    object_apply_mat4() which allows assigning the worldspace matrix in
    python without worrying about the parent.
  * Image editor & texture properties, add new Image, inits 'start' now
  to frame 1 for sequences.
  * Patch [#24608] Fix for typo and better indentation in command line help by Susanne H. (sanne). Thanks!
  * Fix for [#24597] Option External in Smoke cache affects settings of start and end frame of simulation
  * Don't change anything in the pointcache unless a valid external cache is found.
  * Second fix for [#24476] The driver is not displayed in GraphEditor.
  * Texture data still wasn't shown if material didn't have animation data.
  * Also unified the material/texture filtering logic a bit.
  * bugfix [#24583] Mesh.from_pydata does not properly construct faces
* Thu Nov  4 2010 davejplater@gmail.com
- Update to 3rd beta version 2.55.
- Removed blender wrapper as it's no longer necessary.
- Removed pre_checkin.sh - 3rd party blacklisted sources removed.
- Upstream changes:
  * Big improvements - This software has been used extensively in
  production of the Durian open movie project "Sintel".
  * Feature complete - Although some of the 2.5 targets have been
  postponed, such as multi-window support showing multiple scenes
  , a full RNA data level dependency graph, or radial menus.
  * Exciting improvements in Sculpting - Faster, much more stable
  and better brushes.
  * Missing/Incomplete Features - Although really most of it is
  there, not all functionality from 2.4x has been restored yet.
  Some functionality may work in a different way. Some features
  are still slower to use than before.
  * Bugs - We've fixed a lot lately, but there are still quite a
  few bugs. For this second beta around 200 bugs were fixed.
  * Changes - If you're used to the old Blenders, Blender 2.5 may
  seem quite different at first. Be prepared to read a bit about
  this, how to reconfigure things, and learn to use the new
  built-in 2.5 search functionality!
* Sat Jun 26 2010 davejplater@gmail.com
- Fixed bnc#615679 with build flags.
* Wed Jun 23 2010 davejplater@gmail.com
- Update to svn revision 29636 Removed blender-wrapper.patch
* Mon May 17 2010 davejplater@gmail.com
- Update to svn revision 28800 Removed blender-2.48-libtiff.patch
* Sat Jan 23 2010 davejplater@gmail.com
- Cleanup spec file, reinstate fdupes and add blender-2.49b-rpmlintrc
* Sat Dec 19 2009 jengelh@medozas.de
- enable parallel build
* Sat Oct 31 2009 davejplater@gmail.com
-Fixed x-blend.desktop errors and build flags
* Fri Oct 23 2009 davejplater@gmail.com
-Reincorporated pre_checkin.sh script
-Created blender-2.49b-undefined-opp.patch to fix undefined opperation
* Sat Oct 10 2009 crrodriguez@opensuse.org
- blender-2.48a-2.97: possible missing call to close [bnc#523443]
* Sat Sep 19 2009 dave.plater@yahoo.co.uk
- Removed kde3 dependency
* Thu Sep 17 2009 dave.plater@yahoo.co.uk
- Update to blender-2.49b
- Upstream bug fixes :- SoftBody, vertex groups were not notified on deletion & fixes for
  Mass and Spring Painting.
  Softbody, non mesh objects missing initializers [bug #18982].
  Self Shadow Vertex Colors, improved blur method to give more even results.
  Converting nurbs to a mesh ignored smoothing for Alt+C and from python.
  Object Active to Other, Fix python error when running in local view.
  Ancient resource leak where checkPackedFile would open a file and never close it.
  Fix for uninitialized memory use with X11 keyboard and tablet events.
  For more info see :-
  http://www.blender.org/development/release-logs/blender-249/249-update/
* Sat Sep  5 2009 dave.plater@yahoo.co.uk
- Changed blender-doc architecture to noarch
* Sat Aug 29 2009 dave.plater@yahoo.co.uk
- Moved BlenderQuickStart.pdf and blender.html from libdir to docdir
* Tue Aug 18 2009 dave.plater@yahoo.co.uk
- Update to blender-2.49a (bnc#525298)
- fixed uninitialized variables with help from Per Jessen blender-2.49-uninit-var.patch
- blender-doc is now in a seperate package
- New features in Blender-2.49a :-
  Blender player added again
  The Game Engine supports multiple streams of video textures
  for interactive playback in environments
  Real-time Dome rendering
  Game Engine speed-up
  Bullet Physics new features
  Game Engine Modifier support
  Improved Game Logic and Python API
  Texture Nodes
  Projection Painting
  Etch-a-ton armature sketching
  Boolean improvements
  JPEG2000 support
  Python Script extensions
  see http://www.blender.org/development/release-logs/blender-249/.
  for more details of new features in 2.49
* Mon Nov 10 2008 pnemec@suse.cz
- fix memory leak [bnc#442894]
  - new patch blender-2.48-memory_leak.patch
  - upstreamed under blender tracker 17974
* Wed Nov  5 2008 pnemec@suse.cz
- updated to 2.48 [bnc#441453]
  new features:
  - Real-time GLSL Materials
  - Grease Pencil
  - Game Logic
  - Bullet SoftBody
  - Game Engine notes
  - Colored shadows
  - Wind & Deflectors
  - remove upstreamed patches
    blender-2.42a-libtiff.patch
    blender-2.41-undefined_operation.patch
    blender-undefined-op.patch
  - added blender-2.48-uninitialized.patch to
    safe-initialization of pointers
  Fixed security problem [bnc#439121]
  - new patch pythonpath-2.48.patch
* Sun Sep 28 2008 ro@suse.de
- fix build: python version is 2.6
* Tue Sep  2 2008 pnemec@suse.cz
- updated to 2.47
  New tools and improvement have been made to the Snapping tools.
  Better Game Engine logic.
  Fixed an incorrect transformation for particle group visualization.
  Fixed negative value in the Gamma node with negative input.
  Tangent shading (which only affects specular) made bump mapping not work for diffuse.
  Fixed Mesh Deform Modifier not working on extruded curves.
  Fixed crash converting old particle system from a linked file.
  Object instancing didn't restore matrices correct for Environment Map,
  this could give object rendering in the wrong position.
  Compositor nodes with use nodes disabled didn't properly redraw the node window on changes.
- remove unneeded patches blender-python64.patch
  blender-2.41-uninitialized_variables.patch
  blender-2.42a-ffmpeg.patch
* Tue Aug 12 2008 pnemec@suse.cz
- remove doc package contents (now doc is in BuildService)
- repack source without problematic files in /extern direcotory
  [bnc#411821]
* Tue Jun 24 2008 pnemec@suse.cz
- updated to 2.46
  fixed [bnc#393489] (setting czech made blender SIGSEGV)
  remove ugly hack deleting incompatible files [bnc#333796]
  many new features (mouse wheel support, X-ray bones suppor ...
  see www.blender.org for complete list)
* Tue Apr 29 2008 pnemec@suse.cz
- fixed off-by-one problem in previous fix
* Fri Apr 18 2008 pnemec@suse.cz
- security fix (bnc#380922)
  new patch: buffer_overflow_380922-2.45.patch
* Fri Jan  4 2008 pnemec@suse.cz
- do not build againt key_internal.h mt19937int.c [#333796]
* Wed Oct  3 2007 coolo@suse.de
- update to 2.45 to fix compilation with gcc43
* Thu Jul  5 2007 coolo@suse.de
- put desktop file into package
* Tue Jun  5 2007 pnemec@suse.cz
- added script, which repack sources to remove uneeded files
* Tue May 29 2007 pnemec@suse.cz
- blenderplayer is no longer build
- fixing exutable flag on python scripts
- updated to 2.4.4
  - sculpt and multires
  - subsurface scattering
  - new composite nodes
  - character animation
* Thu May 24 2007 stbinner@suse.de
- remove X-SuSE-translate from .desktop file
* Thu Apr 12 2007 pnemec@suse.cz
- Repackaged to remove unused source [#262776]
  Binary unchanged.
* Wed Feb 21 2007 pnemec@suse.cz
- updated to 2.4.3
  added new feature: multi-resolution Meshes,
    multi-level UV, multi-layer images and multi-pass rendering,
    Mesh Sculpt and Retopo painting tools
* Mon Nov  6 2006 schwab@suse.de
- Use RPM_OPT_FLAGS.
- Fix bugs found through this.
- Fix linking of shared libraries.
* Tue Oct 24 2006 pnemec@suse.cz
- clean up spec file
  removed build-fix.patch needed for configuration
- added support for openal
* Mon Oct 23 2006 ro@suse.de
- added freealut-devel to buildrequires
* Fri Oct 20 2006 pnemec@suse.cz
- fix path`s in spec file. Plugins and help is now accesible from
  menu #[213228]
* Tue Oct 17 2006 pnemec@suse.cz
- removed ffmepg from requires
* Mon Oct 16 2006 pnemec@suse.cz
- updated to version 2.42 see Changelog for details
- large enhancement in package, whole specfile rewrited
  all patches either removed or rewrited
- new: support for quick time, better support for yafray
- new: package contains several blender scripts and plugins
* Tue Sep 19 2006 pnemec@suse.cz
- fixed amiguous variable evaluation
  (patch -undefined_operation.patch)
* Wed Sep 13 2006 ro@suse.de
- adde ftgl-devel to BuildRequires
* Thu Jun 29 2006 pnemec@suse.cz
- updated to version 2.41
- fixed some minor problems (uninitialized variables #188166)
  added patch uninitialized_variables.patch, missing_header.patch
- splited doc package, removed old documentation added new one #177578
* Sun Jan 29 2006 aj@suse.de
- Fix BuildRequires.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 16 2006 pnemec@suse.cz
- Updated to version 2.40
- Scons patch moved from spec file to Scons.patch
* Tue Sep 20 2005 pnemec@suse.cz
- remove strict aliasing checking
* Tue Jul 26 2005 sbrabec@suse.cz
- Updated to version 2.37a.
* Wed May 18 2005 yxu@suse.de
- fixed serious compiler warnings
* Mon Apr 25 2005 yxu@suse.de
- Fixed for GCC4.
* Thu Jan  6 2005 sbrabec@suse.cz
- Updated to version 2.36.
* Fri Sep 17 2004 sbrabec@suse.cz
- Added yafray to requires.
- Search language setup, locale and font in /usr/share, not $HOME
  (#45201).
* Thu Sep  2 2004 sbrabec@suse.cz
- Updated to version 2.34.
* Fri Apr  9 2004 sbrabec@suse.cz
- Removed no longer needed LC_CTYPE work-around patch.
  http://projects.blender.org/tracker/?func=detail&atid=125&aid=490&group_id=9
* Sat Mar 13 2004 adrian@suse.de
- remove desktop file copy (use the template from KDE)
* Tue Feb 10 2004 ro@suse.de
- fixed patchfile for lib64 patch
* Fri Feb  6 2004 sbrabec@suse.cz
- Updated to version 2.32.
* Sat Jan 10 2004 adrian@suse.de
- build as user
* Tue Oct  7 2003 ro@suse.de
- use SDL-devel-packages in neededforbuild
* Thu Sep 18 2003 meissner@suse.de
- correct lib64 fix, do not modify buildroot.
* Wed Sep 17 2003 adrian@suse.de
- add menu entry
* Thu Sep 11 2003 sbrabec@suse.cz
- Crash on startup LC_CTYPE work-around (bug #30166, Blender bug #490).
* Thu Sep 11 2003 sbrabec@suse.cz
- Crash on startup fix with Python 2.3 from CVS (bug #30166).
* Thu Aug 21 2003 sbrabec@suse.cz
- Updated to version 2.28a.
* Wed Aug  6 2003 sbrabec@suse.cz
- Updated to version 2.28.
* Thu Jun 12 2003 ro@suse.de
- added directory to filelist
* Tue May 27 2003 ro@suse.de
- remove unpackaged files from buildroot
* Wed May  7 2003 ro@suse.de
- build on python-2.3
* Mon Mar 31 2003 ro@suse.de
- use mesa-devel-packages in neededforbuild
* Wed Feb 19 2003 sndirsch@suse.de
- fixed blendercreator-sample (blendercreator no longer exists;
  it's now called blender)
- therefore renamed blendercreator-sample to blender-sample
- adjusted SuSE menu entries in PDB
* Mon Feb 17 2003 sbrabec@suse.cz
- Updated to version 2.26.
- Workaround of linker segfault.
* Fri Jan 17 2003 sbrabec@suse.cz
- Fixed permissions of blendercreator-sample.
* Wed Jan 15 2003 ro@suse.de
- fix for libpng (needs -lm -lz)
- run autogen.sh
* Wed Jan 15 2003 sbrabec@suse.cz
- Added blendercreator-sample binary and usefull links.
* Tue Jan 14 2003 sbrabec@suse.cz
- Added sample geeko.blend.
- Moved documentation to subdir PublisherDoc.
- Removed blendermodule.
* Tue Nov 26 2002 sbrabec@suse.cz
- Workaround biarch bugs in python.m4 (bug 22011) and libtool search
  paths (bug 22010).
* Wed Nov 20 2002 sbrabec@suse.cz
- Added official Blender documentation.
* Tue Nov  5 2002 sbrabec@suse.cz
- Added first public GPL release with unofficial automake support.
