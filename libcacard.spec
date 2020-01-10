Name:		libcacard
Version:	2.5.2
Release:	2%{?dist}
Epoch:      40
Summary:	Common Access Card (CAC) Emulation

Group:		Development/Libraries
License:	GPLv2+ and LGPLv2+ and BSD
URL:		http://www.spice-space.org/page/Libcacard
Source0:	http://www.spice-space.org/download/libcacard/libcacard-2.5.2.tar.xz


BuildRequires: glib2-devel
BuildRequires: nss-devel

Obsoletes: libcacard-rhev

%description
Common Access Card (CAC) emulation library.


%package    tools
Summary:        CAC Emulation tools
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}
Obsoletes: libcacard-tools-rhev

%description tools
CAC emulation tools.


%package devel
Summary:        CAC Emulation devel
Group:          Development/Libraries
Requires:       libcacard = %{epoch}:%{version}-%{release}
Obsoletes: libcacard-devel-rhev

%description devel
CAC emulation development files.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags} 


%install
%make_install

find $RPM_BUILD_ROOT -name "libcacard.so*" -exec chmod +x \{\} \;
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%check
make check V=1

%files
%defattr(-,root,root,-)
%{_libdir}/libcacard.so.*

%files tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%files devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc


%changelog
* Fri Mar 18 2016 Miroslav Rezanina <mrezanin@redhat.com> - 2.5.2-2.el7
- Obsolete libcacard-rhev (bz#1315953)

* Fri Jan 29 2016 Miroslav Rezanina <mrezanin@redhat.com> - 2.5.2-1.el7
- Initial build
