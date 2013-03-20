#
# spec file for package Field3D
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Asterios Dramis <asterios.dramis@gmail.com>.
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

#%define so_ver 1_4
%define release_prefix 1

Name:           Field3D
Version:        1.4.0
Release:        %{?release_prefix}.0%{?dist}
Summary:        Library for Storing Voxel Data
License:        BSD-3-Clause
Group:          Productivity/Graphics/Other
Url:            https://sites.google.com/site/field3d/
# http://github.com/imageworks/Field3D/tarball/v1.3.2
Source0:        %{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM Field3D-1.3.2-libboost.patch asterios.dramis@gmail.com -- Fix boost linking (patch taken from Fedora)
Patch0:         Field3D-1.3.2-libboost.patch
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  hdf5-devel
%if 0%{?suse_version} > 1220
BuildRequires:  ilmbase-devel
%else
BuildRequires:  libilmbase-devel
%endif
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Field3D is an open source library for storing voxel data. It provides C++
classes that handle in-memory storage and a file format based on HDF5 that
allows the C++ objects to be written to and read from disk.

%package devel
Summary:        Development Files for Field3D
Group:          Development/Libraries/C and C++
Requires:       libField3D = %{version}

%description devel
This package provides development libraries and headers needed to build
software using Field3D.

%package -n libField3D
Summary:        Library for Storing Voxel Data
Group:          System/Libraries

%description -n libField3D
Field3D is an open source library for storing voxel data. It provides C++
classes that handle in-memory storage and a file format based on HDF5 that
allows the C++ objects to be written to and read from disk.

%prep
%setup -q
#%patch0 -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
__libsuffix=$(echo %_lib | cut -b4-)
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB_SUFFIX="$__libsuffix" \
    -DBUILD_SHARED_LIBS=ON \
    -DINSTALL_DOCS=OFF \
    ..
make %{?_smp_mflags} VERBOSE=1
cd ..

%install
%make_install -C build

install -Dpm 0644 man/f3dinfo.1 %{buildroot}%{_mandir}/man1/f3dinfo.1

# Install devel docs (do it manually to fix also rpmlint warning "files-duplicate" with %%fdupes)
mkdir -p %{buildroot}%{_docdir}/%{name}-devel
cp -a docs/html/ %{buildroot}%{_docdir}/%{name}-devel/

%fdupes -s %{buildroot}

%post -n libField3D -p /sbin/ldconfig

%postun -n libField3D -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README
%{_bindir}/*
%{_mandir}/man1/f3dinfo.1%{ext_man}

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-devel/
%{_includedir}/Field3D/
%{_libdir}/*.so

%files -n libField3D
%defattr(-,root,root,-)
%{_libdir}/libField3D.so.1.4*

%changelog
* Wed Mar 20 2013 Freeman Zhang <zhanggyb@gmail.com>
- Update to 1.4.0
- Rename to libField3D instead of libField3D1_3

* Tue Feb 19 2013 asterios.dramis@gmail.com
- Initial release (version 1.3.2).
- Added a patch (Field3D-1.3.2-libboost.patch) to fix boost linking (patch
  taken from Fedora).

