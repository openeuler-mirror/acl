Name:          acl
Version:       2.2.53
Release:       4
Summary:       Commands for manipulating POSIX access control lists

License:       GPLv2+ and LGPLv2+
URL:           https://savannah.nongnu.org/projects/acl
Source0:       http://download.savannah.nongnu.org/releases/acl/acl-2.2.53.tar.gz

BuildRequires: libattr-devel gawk libtool gettext
Conflicts:     filesystem < 3
Provides:      libacl%{?_isa} libacl
Obsoletes:     libacl

%description
This package contains commands for manipulating POSIX access control lists,
and the libacl.so dynamic library which contains the POSIX 1003.1e draft
standard 17 functions for manipulating access control lists.


%package devel
Summary:       Files necessary to develop applications with libacl
License:       LGPLv2+
Requires:      acl = %{version}-%{release}, libattr-devel
Provides:      libacl-devel
Obsoletes:     libacl-devel

%description devel
This package contains header files for the POSIX ACL library.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
%make_build

%install
%make_install
%delete_la_and_a
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

%find_lang %{name}

%check
# permissions.test needs 'daemon' users to be in the 'bin' group. If not, stop this test.
if test 0 = "$(id -u)"; then
    sed -e 's|test/root/permissions.test||' -i test/Makemodule.am Makefile.in Makefile
fi
# setfacl.test needs 'bin' users to have the access to build dir. If not, stop this test.
if ! runuser -u bin -- "${PWD}/setfacl" --version; then
    sed -e 's|test/root/setfacl.test||' -i test/Makemodule.am Makefile.in Makefile
fi

make check

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license doc/COPYING*
%{_bindir}/*acl
%{_libdir}/libacl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/libacl.pc

%files help
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Sat Dec 14 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-4
- Provides arch releated rpm

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-3
- Package init

