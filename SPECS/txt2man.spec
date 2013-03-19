Summary:	Converts flat ASCII text to man page forma
Name:		txt2man
Version:	1.5.6
Release:	3.1
License:	GPLv3
Group:		Development/Tools/Doc Generators
URL:		http://mvertes.free.fr/ 

BuildArch:      noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-build
Source1:	txt2man
Source2:	txt2man.1
Requires:	gawk

%description
Txt2man converts flat ASCII text to man page format. It is a shell
script using gnu awk, that should run on any Unix like system.

%prep

%build

%install
install -d -m 0755 %{buildroot}/%{_bindir}
install -d -m 0755 %{buildroot}/%{_mandir}/man1
install -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/%{name}
install -m 0644 %{SOURCE2} %{buildroot}/%{_mandir}/man1/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}

%changelog
* Sat May 1 2011 Stefan Jakobs <stefan.jakobs@rus.uni-stuttgart.de> - 1.5.6
- initial release
