# Filter provides from Python libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

%define release_prefix 1

%global cmake cmake -DCMAKE_SKIP_RPATH=OFF

Name:           OpenColorIO
Version:        1.0.8
Release:        %{?release_prefix}.2%{?dist}
Summary:        Enables color transforms and image display across graphics apps

Group:		Development/Libraries
License:        BSD
URL:            http://opencolorio.org/
# Github archive was generated on the fly using the following URL:
# https://github.com/imageworks/OpenColorIO/tarball/v1.0.8
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  help2man

# Libraries
BuildRequires:  python-devel
BuildRequires:  Mesa-libGL-devel
#BuildRequires:	mesa-libGLU-devel	# not found in openSuSE 12.3
BuildRequires:  libX11-devel libXmu-devel libXi-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  zlib-devel

#######################
# Unbundled libraries #
#######################
BuildRequires:  tinyxml-devel
BuildRequires:  liblcms2-devel
BuildRequires:  yaml-cpp-devel >= 0.3.0

# The following bundled projects  are only used for document generation.
#BuildRequires:  python-docutils
#BuildRequires:  python-jinja2
#BuildRequires:  python-pygments
#BuildRequires:  python-setuptools
#BuildRequires:  python-sphinx


%description
OCIO enables color transforms and image display to be handled in a consistent
manner across multiple graphics applications. Unlike other color management
solutions, OCIO is geared towards motion-picture post production, with an
emphasis on visual effects and animation color pipelines.


%package doc
BuildArch:      noarch
Summary:        API Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
API documentation for %{name}.


%package devel
Summary:        Development libraries and headers for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.


%prep
%setup -q

# Remove what bundled libraries
rm -f ext/lcms*
rm -f ext/tinyxml*
rm -f ext/yaml*

%build
rm -rf build && mkdir build && pushd build
cmake	-D CMAKE_BUILD_TYPE=Release \
	-D CMAKE_PREFIX_PATH=%_prefix \
	-D CMAKE_INSTALL_PREFIX=%_prefix \
	-D OCIO_BUILD_STATIC=OFF \
	-D PYTHON_INCLUDE_LIB_PREFIX=OFF \
	-D OCIO_BUILD_DOCS=ON \
	-D OCIO_BUILD_TESTS=ON \
	-D OCIO_LINK_PYGLUE=ON \
	-D OCIO_PYGLUE_SONAME=OFF \
	-D USE_EXTERNAL_YAML=TRUE \
	-D USE_EXTERNAL_TINYXML=TRUE \
	-D USE_EXTERNAL_LCMS=TRUE \
%ifarch x86_64
	-D LIB_SUFFIX=64 \
%endif
%ifnarch x86_64
	-D OCIO_USE_SSE=OFF \
%endif
       ../

make %{?_smp_mflags}


%install
pushd build
make install DESTDIR=%{buildroot}

# Generate man pages
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociocheck.1 \
         src/apps/ociocheck/ociocheck
help2man -N -s 1 %{?fedora:--version-string=%{version}} \
         -o %{buildroot}%{_mandir}/man1/ociobakelut.1 \
         src/apps/ociobakelut/ociobakelut


%check
# Testing passes locally in mock but fails on the fedora build servers.
#pushd build && make test


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc ChangeLog LICENSE README
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_datadir}/ocio
%{_datadir}/ocio/setup_ocio.sh
%{_mandir}/man1/*
%{python_sitearch}/*.so

%files doc
%{_prefix}/share/doc/%{name}
%doc %{_docdir}/%{name}/

%files devel
%{_includedir}/OpenColorIO/
%{_includedir}/PyOpenColorIO/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Mar 19 2013 Freeman Zhang <zhanggyb@gmail.com> - 1.0.8-2
- Build for openSuSE 12.3

* Tue Dec 11 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.8-1
- Update to latest upstream release.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-4
- Only use SSE instructions on x86_64.

* Wed Apr 25 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-3
- Misc spec cleanup for packaging guidelines.
- Disable testing for now since it fails on the build servers.

* Wed Apr 18 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.7-1
- Latest upstream release.

* Thu Apr 05 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0.6-1
- Latest upstream release.

* Wed Nov 16 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0.2-1
- Initial release.
