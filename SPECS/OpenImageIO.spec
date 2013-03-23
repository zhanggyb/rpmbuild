# OBS Release tag, needs to be here!!!
%define release_prefix 1

Name:           OpenImageIO
Version:        1.1.7
Release:        %{?release_prefix}.3%{?dist}
Summary:        Library for reading and writing images

Group:          Development/Libraries
License:        BSD
URL:            https://sites.google.com/site/openimageio/home

		# git archive Release-1.1.7 --prefix=oiio-Release-1.1.7/ -o oiio-Release-1.1.7.tar.gz
Source0:        oiio-Release-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:	txt2man
BuildRequires:  libqt4-devel
BuildRequires:  Mesa-libGL-devel
BuildRequires:  boost-devel
BuildRequires:  glew-devel
BuildRequires:  openexr-devel
BuildRequires:	ilmbase-devel
BuildRequires:  python-devel
BuildRequires:  libpng15-devel
BuildRequires:	libtiff-devel
BuildRequires:	openjpeg-devel
BuildRequires:	libwebp-devel
BuildRequires:  zlib-devel
BuildRequires:  libjasper-devel
#BuildRequires:  pugixml-devel
BuildRequires:  tbb-devel
BuildRequires:  hdf5-devel
#BuildRequires: opencv-devel
#BuildRequires:	Field3D-devel
BuildRequires:  OpenColorIO-devel

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}


%description
OpenImageIO is a library for reading and writing images, and a bunch of related
classes, utilities, and applications. Main features include:
- Extremely simple but powerful ImageInput and ImageOutput APIs for reading and
  writing 2D images that is format agnostic.
- Format plugins for TIFF, JPEG/JFIF, OpenEXR, PNG, HDR/RGBE, Targa, JPEG-2000,
  DPX, Cineon, FITS, BMP, ICO, RMan Zfile, Softimage PIC, DDS, SGI,
  PNM/PPM/PGM/PBM, Field3d.
- An ImageCache class that transparently manages a cache so that it can access
  truly vast amounts of image data.


%package utils
Summary:        Command line utilies for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Command-line tools to minipulate and get information on images using the
%{name} library.

%package doc
Summary:	Documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description doc
Documentation for package %{name}.

%package iv
Summary:        %{name} based image viewer.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description iv
A really nice image viewer, iv, based on %{name} classes (and so will work with
any formats for which plugins are available).


%package devel
Summary:        Library and API for programming %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for package %{name}


%prep
%setup -q -n oiio-Release-%{version}

echo %{_datadir}

%build
rm -rf build/linux && mkdir -p build/linux && pushd build/linux
# CMAKE_SKIP_RPATH is OK here because it is set to FALSE internally and causes
# CMAKE_INSTALL_RPATH to be cleared, which is the desiered result.
cmake	-D CMAKE_BUILD_TYPE=Release \
	-D CMAKE_PREFIX_PATH=%{_prefix} \
	-D CMAKE_INSTALL_PREFIX=%{_prefix} \
	-D USE_QT=ON \
	-D USE_OPENGL=ON \
	-D CMAKE_SKIP_RPATH:BOOL=TRUE \
	-D INCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
	-D PYLIB_INSTALL_DIR:PATH=%{python_sitearch} \
	-D INSTALL_DOCS:BOOL=TRUE \
	-D USE_EXTERNAL_PUGIXML:BOOL=FALSE \
	-D CMAKE_CXX_FLAGS="-fPIC" \
	-D USE_TBB:BOOL=TRUE \
	-D USE_EXTERNAL_TBB=TRUE \
%ifarch x86_64
	-D LIB_INSTALL_DIR=%{_prefix}/lib64 \
%endif
%ifarch ppc %{power64}
	-D NOTHREADS:BOOL=TRUE \
%endif
       ../../src

make %{?_smp_mflags}


%install
pushd build/linux
make DESTDIR=%{buildroot} install

# Move man pages to the right directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -a doc/*.1 %{buildroot}%{_mandir}/man1

# Move pdf
mkdir -p %{buildroot}%{_datadir}/doc/packages/%{name}-doc/
mv %{buildroot}%{_datadir}/doc/openimageio/*.pdf %{buildroot}%{_datadir}/doc/packages/%{name}-doc/
rm -rf %{buildroot}%{_datadir}/doc/openimageio

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%check
#pushd build/linux && make test


%files
%{_libdir}/libOpenImageIO.so.*
%{python_sitearch}/OpenImageIO.so

%files doc
%doc CHANGES LICENSE
%{_datadir}/doc

%files utils
%exclude %{_bindir}/iv
%{_bindir}/*
%exclude %{_mandir}/man1/iv.1.gz
%{_mandir}/man1/*.1.gz

%files iv
%{_bindir}/iv
%{_mandir}/man1/iv.1.gz

%files devel
%{_libdir}/libOpenImageIO.so
%{_includedir}/*


%changelog
* Fri Mar 22 2013 Freeman Zhang <zhanggyb@gmail.com> - 1.1.7-1.3
- Use external tbb, remove opencv requirement
- repack doc
- Use external tbb-devel

* Tue Mar 19 2013 Freeman Zhang <zhanggyb@gmail.com> - 1.1.7
- Update the 1.1.7
- build for openSuSE 12.3

* Wed Feb 20 2013  Dan Eicher <dan@trollwerks.org> - 1.1.6-1
- Update to latest upstream release.

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.1.3-5
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.1.3-4
- Rebuild for Boost-1.53.0

* Mon Jan 28 2013 Karsten Hopp <karsten@redhat.com> 1.1.3-3
- update PPC patch, use power64 macro

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.1.3-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Jan 14 2013 Richard Shaw <hobbes1069@gmail.com> - 1.1.3-1
- Update to latest upstream release.
- Separate utilities and library packages.

* Fri Dec 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-3
- Rebuild, see
  http://lists.fedoraproject.org/pipermail/devel/2012-December/175685.html

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 1.0.9-2
- Rebuild for glew 1.9.0

* Sat Sep 22 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.9-1
- Update to latest upstream release.

* Wed Aug  8 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.8-2
- rebuild against boost-1.50

* Wed Aug 01 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-1
- Update to latest upstream release.

* Mon Jul 30 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-3
- Rebuild for updated libGLEW.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-1
- Update to latest upstream release.

* Thu Jun 28 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.6-1
- Update to latest upstream release.
- Fix linking against TBB which broke at some point.

* Tue Jun 12 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.5-1
- Update to latest upstream release.

* Mon May 07 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.4-2
- Rebuild for updated libtiff.
- Add OpenColorIO to build requirements.

* Thu May 03 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.4-1
- Update to latest upstream release.

* Tue Apr 24 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.3-1
- Update to latest upstream release.

* Fri Mar 02 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.0-1
- Update to latest upstream release.

* Thu Jan 05 2012 Richard Shaw <hobbes1069@gmail.com> - 0.10.4-1
- Update to 0.10.4.
- Rebuild for GCC 4.7.0.

* Fri Dec 02 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.3-1
- Build against TBB library.

* Sat Nov 05 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.3-1
- Update to 0.10.3
- Rebuild for libpng 1.5.
- Fixed bulding against tbb library.

* Thu Aug 27 2011 Tom Callaway <spot@fedoraproject.org> - 0.10.2-1
- Update to 0.10.2

* Thu Aug 04 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.1-2
- New upstream release.
- Fix private shared object provides with python library.

* Mon Jul 18 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.0-2
- Disabled use of the TBB library.
- Moved headers to named directory.

* Tue Jul 05 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.0-1
- Inital Release.

