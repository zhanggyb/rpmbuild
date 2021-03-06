# OpenShadingLanguage rpmbuild spec

%define release_prefix 1

Name:           OpenShadingLanguage
Version:        1.3.0
Release:        %{?release_prefix}.1%{?dist}
Summary:        Open Shading Language (OSL) is a language for programmable shading in renderers and other applications

Group:          Development/Libraries
License:        New BSD
URL:            http://code.google.com/p/openshadinglanguage/

# source url: https://github.com/imageworks/OpenShadingLanguage/
Source0:        OpenShadingLanguage-Release-%{version}.tar.gz
Patch0:		OSL-%{version}-fix-cmake.patch

BuildRequires:  cmake
BuildRequires: flex
BuildRequires: bison
BuildRequires:  boost-devel
BuildRequires:  openexr-devel
BuildRequires: ilmbase-devel
BuildRequires: tbb-devel
BuildRequires: llvm-devel
BuildRequires:  OpenColorIO-devel
BuildRequires: OpenImageIO-devel
# BuildRequires: partio

%description
Open Shading Language (OSL) is a small but rich language for programmable shading in 
advanced renderers and other applications, ideal for describing materials, lights, 
displacement, and pattern generation.

OSL was developed by Sony Pictures Imageworks for use in its in-house renderer used for 
feature film animation and visual effects. The language specification was developed with 
input by other visual effects and animation studios who also wish to use it.

OSL is robust and production-proven, and was the exclusive shading system for big VFX 
films such as "Men in Black 3: and "The Amazing Spider-Man," animated features such 
as "Hotel Transylvania", and several other films currently in production.

The OSL code is distributed under the "New BSD" license (see the "LICENSE" file that 
comes with the distribution), and the documentation under the Creative Commons 
Attribution 3.0 Unported License (http://creativecommons.org/licenses/by/3.0/). In short, 
you are free to use OSL in your own applications, whether they are free or commercial, 
open or proprietary, as well as to modify the OSL code and documentation as you desire, 
provided that you retain the original copyright notices as described in the license. 


%package doc
Summary:	Documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description doc
Documentation for package %{name}.

%package devel
Summary:	Header files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for developing on %{name}.

%prep
%setup -q -n OpenShadingLanguage-Release-%{version}
%patch0 -p1

%build
rm -rf build/linux && mkdir -p build/linux && pushd build/linux
__libsuffix=$(echo %_lib | cut -b4-)

cmake	-D CMAKE_BUILD_TYPE=Release \
	-D CMAKE_PREFIX_PATH=%{_prefix} \
	-D CMAKE_INSTALL_PREFIX=%{_prefix} \
	-D LLVM_STATIC:BOOL=TRUE \
	-D CMAKE_SKIP_RPATH:BOOL=TRUE \
	-D USE_PARTIO:BOOL=FALSE \
	-D LIB_SUFFIX="$__libsuffix" \
	-D USE_TBB:BOOL=TRUE \
       ../../src

make %{?_smp_mflags}

popd

%install
pushd build/linux
make DESTDIR=%{buildroot} install
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
#pushd build/linux && make test


%files
%defattr(-,root,root,-)
%_prefix/*
%exclude %{_includedir}
%exclude %{_datadir}/doc

%files doc
%{_datadir}/doc/*

%files devel
%{_includedir}/*


%changelog
* Fri Mar 22 2013 Freeman Zhang <zhanggyb@gmail.com>
- Version 1.3.0
- Inital Release.

