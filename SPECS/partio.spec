#
# spec file for package partio
#

%define release_prefix 1

Name:           partio
Version:        1.1.0
Release:        %{?release_prefix}.0%{?dist}
Summary:        Partio - A library for particle IO and manipulation
License:        BSD-3-Clause
Group:          Productivity/Graphics/Other

Url:            https://github.com/wdas/partio
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  freeglut-devel
BuildRequires:  libX11-devel
BuildRequires:  Mesa-libGL-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Partio is a library for particle IO and manipulation, developed by Walt Disney Animation Studios

%prep
%setup -q

%build
__libsuffix=$(echo %_lib | cut -b4-)

rm -rf build && mkdir -p build && pushd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB_SUFFIX="$__libsuffix" \
    ..
make %{?_smp_mflags} VERBOSE=1
popd

%install
%make_install -C build

%post

%postun

%files
%defattr(-,root,root,-)
%{_prefix}/*

%changelog
* Wed Mar 20 2013 Freeman Zhang <zhanggyb@gmail.com>
- Version 1.1.0
- Initial release

