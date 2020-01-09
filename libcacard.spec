Name:           libcacard
Version:        0.15.0

Release:        2%{?dist}
Summary:        Common Access Card (CAC) Emulation
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.qemu.org/
Source0:        http://wiki.qemu.org/download/qemu-%{version}.tar.gz
BuildRequires:  nss-devel >= 3.12 libtool glib2-devel
Patch00:        0001-drop-zlib-check.patch
Patch01:        0002-libcacard-vcard_emul_nss-support-cards-lying-about-C.patch
Patch02:        0003-libcacard-don-t-leak-vcard_emul_alloc_arrays-mem.patch
Patch03:        0004-libcacard-s-strip-args-strip-args-1.patch
Patch04:        0005-libcacard-fix-soft-.-parsing-in-vcard_emul_options.patch
Patch05:        0006-libcacard-introduce-NEXT_TOKEN-macro.patch
Patch06:        0007-libcacard-replace-copy_string-with-strndup.patch
Patch07:        0008-libcacard-add-pc-file-install-it-includes.patch
Patch08:        0009-libcacard-use-INSTALL_DATA-for-data.patch
Patch09:        0010-Fix-spelling-in-comments-and-debug-messages-recieve-.patch
Patch10:        0011-Improvements-to-libtool-support.patch
Patch11:        0012-Silence-make-if-nothing-is-to-do-for-libcacard.patch
Patch12:        0013-libcacard-cac-fix-typo-in-cac_delete_pki_applet_priv.patch
Patch13:        0014-libcacard-vscclient-fix-error-paths-for-socket-creat.patch

ExclusiveArch:  i686 x86_64

%description
Common Access Card (CAC) emulation library.

%package tools
Summary:        CAC Emulation tools
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description tools
CAC emulation tools.

%package devel
Summary:        CAC Emulation devel
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
CAC emulation development files.

%prep
%setup -n qemu-%{version} -q
%patch00 -p1
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} --disable-guest-agent --target-list=x86_64-softmmu

# make sure libcacard.txt is the README
cp -f docs/libcacard.txt README

make libcacard.la %{?_smp_mflags}
make -C libcacard vscclient

%install
rm -rf $RPM_BUILD_ROOT
make install-libcacard DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libcacard.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/pkgconfig/libcacard.pc
%{_libdir}/libcacard.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%changelog
* Tue Oct 11 2011 Alon Levy <alevy@redhat.com> - 0.15.0
 - not a rebase - no changes in libcacard subdirectory
   between 0.15.0-rc0 and 0.15.0 in the upstream package.
  - but allows the fedora and RHEL package to remain in sync
    on a released version.
 - dropped zlib dep which was only required for configure phase
   via added patch 0001-drop-zlib-check.patch
 - added three patches that only cleanup the build process
   0010-Fix-spelling-in-comments-and-debug-messages-recieve-.patch
   0011-Improvements-to-libtool-support.patch
   0012-Silence-make-if-nothing-is-to-do-for-libcacard.patch
 - Final two patches resolve the bug 727916:
   0013-libcacard-cac-fix-typo-in-cac_delete_pki_applet_priv.patch
   0014-libcacard-vscclient-fix-error-paths-for-socket-creat.patch
 - Resolves: rhbz#727916

* Thu Jul 28 2011 Alon Levy <alevy@redhat.com> - 0.14.90-2
 - fix permissions of h files to not change because of rebase.
 - change NVR to match libcacard.so
   - will change when qemu-0.15.0 is released.
 - Copied correct README
 - Resolves: rhbz#723895

* Tue Jul 26 2011 Alon Levy <alevy@redhat.com> - 0.15.0-rc0
- upstream update, it is now qemu based, so build process changed, and version to match.
 - no non-rc release yet of qemu with required patches, hence using rc0. There are still
   some patches carried here that hopefully will get into 0.15.0 or 0.16.0 in the latest.
 - upstream updated to 0.15.0-rc0
 - resolves rhbz#723895

* Fri Feb 04 2011 Uri Lublin <uril@redhat.com> - 0.1.2-2
 - ExclusiveArch:  i686 x86_64
  Resolves: rhbz#663063

* Thu Feb 03 2011 Alon Levy <alevy@redhat.com> - 0.1.2-1
 - bump version to 0.1.2
 - style fixes
 - vscclient.c: fix tabulation
  - add copyright header
  - send init on connect, only start vevent thread on response
  - use hton,ntoh
  - read payload after header check, before type switch
  - update for vscard_common changes, empty Flush implementation
 - vcard_emul_nss: load coolkey in more situations
 - vscard_common.h:
  - VSCMsgInit capabilities and magic
  - VSCMsgReconnect stringified
  - define VSCARD_MAGIC
  - update copyright
  - fix message type enum
 - bump version to 0.1.1
  - vcard_emul,vcard_emul_nss
   - add VCARD_EMUL_INIT_ALREADY_INITED
   - add vcard_emul_replay_insertion_events
 - vreader: add vreader_queue_card_event
  Resolves: rhbz#663063

* Thu Dec 16 2010 Hans de Goede <hdegoede@redhat.com> - 0.1.0-5
- Build for RHEL-6
  Resolves: rhbz#663063

* Sun Dec 12 2010 Alon Levy <alevy@redhat.com> - 0.1.0-4
- address review issues:
 - Group for main and devel and tools
 - Requires for devel and tools
- fix changelog for previous entry (day was wrong, and macro quoting)
* Sat Dec 11 2010 Alon Levy <alevy@redhat.com> - 0.1.0-3
- address review issues: defattr typo, %%doc at %%files, remove .*a from install
* Thu Dec 9 2010 Alon Levy <alevy@redhat.com> - 0.1.0-2
- address prereview issues.
* Thu Dec 9 2010 Alon Levy <alevy@redhat.com> - 0.1.0-1
- initial package.

