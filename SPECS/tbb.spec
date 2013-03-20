#
# spec file for package tbb
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


%define so_ver 2

Name:           tbb
Version:        41_20130116
Release:        1.1
License:        GPL-2.0
Summary:        Threading Building Blocks (TBB)
Url:            http://threadingbuildingblocks.org/
Group:          System/Libraries
Source0:        http://threadingbuildingblocks.org/sites/default/files/software_releases/source/%{name}%{version}oss_src.tgz
# PATCH-FIX-OPENSUSE optflags.patch -- Use rpm optflags
Patch0:         optflags.patch
# PATCH-FIX-UPSTREAM tbb-4.0-cas.patch asterios.dramis@gmail.com -- Fix build on PowerPC, http://software.intel.com/en-us/forums/showthread.php?t=106373 (taken from Fedora)
Patch1:         tbb-4.0-cas.patch
BuildRequires:  gcc-c++
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  %ix86 ia64 x86_64 ppc ppc64

%description
Threading Building Blocks (TBB) offers a rich and complete approach to
expressing parallelism in a C++ program. It is a library that helps you take
advantage of multi-core processor performance without having to be a threading
expert. Threading Building Blocks is not just a threads-replacement library. It
represents a higher-level, task-based parallelism that abstracts platform
details and threading mechanism for performance and scalability.

%package -n libtbb%{so_ver}
Summary:        Threading Building Blocks (TBB)
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n libtbb%{so_ver}
Threading Building Blocks (TBB) offers a rich and complete approach to
expressing parallelism in a C++ program. It is a library that helps you take
advantage of multi-core processor performance without having to be a threading
expert. Threading Building Blocks is not just a threads-replacement library. It
represents a higher-level, task-based parallelism that abstracts platform
details and threading mechanism for performance and scalability.

%package -n libtbbmalloc%{so_ver}
Summary:        Threading Building Blocks (TBB)
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n libtbbmalloc%{so_ver}
Threading Building Blocks (TBB) offers a rich and complete approach to
expressing parallelism in a C++ program. It is a library that helps you take
advantage of multi-core processor performance without having to be a threading
expert. Threading Building Blocks is not just a threads-replacement library. It
represents a higher-level, task-based parallelism that abstracts platform
details and threading mechanism for performance and scalability.

%package devel
Summary:        Development Files for Threading Building Blocks (TBB)
Group:          Development/Libraries/C and C++
Requires:       c++_compiler
Requires:       libtbb%{so_ver} = %{version}
Requires:       libtbbmalloc%{so_ver} = %{version}

%description devel
Threading Building Blocks (TBB) offers a rich and complete approach to
expressing parallelism in a C++ program. It is a library that helps you take
advantage of multi-core processor performance without having to be a threading
expert. Threading Building Blocks is not just a threads-replacement library. It
represents a higher-level, task-based parallelism that abstracts platform
details and threading mechanism for performance and scalability.

This package contains the header files needed for development with tbb.

%prep
%setup -q -n %{name}%{version}oss
%patch0
%patch1 -p1

%build
make OPTFLAGS="%{optflags}" %{?_smp_mflags} tbb_build_prefix=obj

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
pushd include
    find tbb -type f -name \*.h -exec \
        install -Dpm 644 {} %{buildroot}%{_includedir}/{} \
    \;
popd
pushd build/obj_release
    for file in libtbb{,malloc{,_proxy}}; do
        install -Dpm 0755 ${file}.so.%{so_ver} %{buildroot}%{_libdir}
        ln -s $file.so.%{so_ver} %{buildroot}%{_libdir}/$file.so
    done
popd

%post -n libtbb%{so_ver} -p /sbin/ldconfig

%postun -n libtbb%{so_ver} -p /sbin/ldconfig

%post -n libtbbmalloc%{so_ver} -p /sbin/ldconfig

%postun -n libtbbmalloc%{so_ver} -p /sbin/ldconfig

%files -n libtbb%{so_ver}
%defattr(-,root,root,-)
%{_libdir}/libtbb.so.%{so_ver}*

%files -n libtbbmalloc%{so_ver}
%defattr(-,root,root,-)
%{_libdir}/libtbbmalloc.so.%{so_ver}*
%{_libdir}/libtbbmalloc_proxy.so.%{so_ver}*

%files devel
%defattr(-,root,root,-)
%doc CHANGES COPYING index.html
%doc doc/Release_Notes.txt doc/html/
%{_includedir}/tbb/
%{_libdir}/libtbb.so
%{_libdir}/libtbbmalloc.so
%{_libdir}/libtbbmalloc_proxy.so

%changelog
* Sun Feb 17 2013 asterios.dramis@gmail.com
- Update to version 41_20130116:
  * See CHANGES file for news.
- Removed tbb package which included only doc files (moved them to tbb-devel).
- Updated optflags.patch to make it apply correctly and also fix "File is
  compiled without RPM_OPT_FLAGS" rpm post build check warning.
- Added a patch "tbb-4.0-cas.patch" to fix build on PowerPC (taken from
  Fedora).
* Sun Jan 29 2012 jengelh@medozas.de
- Remove redundant tags/sections per specfile guideline suggestions
- Parallel building using %%_smp_mflags
* Sun Aug 14 2011 crrodriguez@opensuse.org
- Update to version tbb30_20110704
* Wed Sep 16 2009 meissner@suse.de
- Reimport from Andi Kleens directory.
* Sat Sep  5 2009 andi@firstfloor.org
- update to 22_20090809oss, install machine/* includes
* Thu Sep 11 2008 skh@suse.de
- update to snapshot 21_20080825 (for details see CHANGES file in
  package)
- remove obsolete patch tbb-build.patch
- split off libtbb2 and libtbbmalloc2 subpackages
* Wed Aug 13 2008 ro@suse.de
- add ExclusiveArch
* Mon Apr 28 2008 skh@suse.de
- update to source version tbb20_20080408oss_src
* Wed Feb 13 2008 dmueller@suse.de
- fix buildrequires
* Fri Feb  8 2008 skh@suse.de
- initial package from version 2.0, source version
  tbb20_20080122oss_src
