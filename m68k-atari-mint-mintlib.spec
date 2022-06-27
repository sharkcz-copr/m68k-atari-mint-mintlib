# we are cross-compiled libraries
%global debug_package %{nil}
%global __strip /bin/true

%global cvsdate 20140312

Name:           m68k-atari-mint-mintlib
Summary:        Necessary files from the MiNTLib
Version:        0.60.1
Release:        2.%{cvsdate}cvs%{?dist}
License:        LGPL+
URL:            https://github.com/freemint/mintlib
#Source0:        http://vincent.riviere.free.fr/soft/m68k-atari-mint/archives/mintlib-CVS-%%{cvsdate}.tar.gz
# use my https enabled mirror instead
Source0:        https://fedora.danny.cz/atari/mintlib-CVS-%{cvsdate}.tar.gz
# workaround http://gcc.gnu.org/bugzilla/show_bug.cgi?id=52714 by using -O0 for debug build
Patch0:         mintlib-CVS-20111028-flags.patch
BuildArch:      noarch
BuildRequires:  m68k-atari-mint-gcc
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  gcc
BuildRequires:  make
Requires:       m68k-atari-mint-filesystem


%description
This package allows to use the MiNTLib libraries for cross-compiling.
Of course you also need to install adequate cross tools like cross
linker, cross assembler and not to forget a cross compiler. Both the
binutils (linker and assembler) and the cross compiler (preferably
gcc) can be built for the target mint with the native compiler on
the cross platform.
 
This package itself contains only docs.  The headers are contained in
the package mintlib-devel.  So are the standard static libraries.
You have to install both the libraries and the headers before you
start to build the cross compiler (unless the cross compiler is also
available as binary rpm).


%prep
%setup -q -n mintlib-CVS-%{cvsdate}
%patch0 -p1 -b .flags

find . -type f -exec chmod -x {} \;
chmod a+x move-if-change mintlib/gensys mkinstalldirs


%build
make prefix=%{mint_prefix} CROSS=yes \
	WITH_020_LIB=yes WITH_V4E_LIB=yes \
	WITH_DEBUG_LIB=yes WITH_PROFILE_LIB=no \
	toolprefix=%{mint_target}-


%install
make install prefix=$RPM_BUILD_ROOT%{mint_prefix} \
           HEADER_CLEANUP=no \
           TZTOPDIR=$RPM_BUILD_ROOT%{mint_prefix} \
           bootsbindir=$RPM_BUILD_ROOT/%{mint_sbindir} \
           REDO=none CROSS=yes

# cleanup
rm -rf $RPM_BUILD_ROOT%{mint_mandir}


%files
%doc AUTHORS BUGS COPYING COPYING.LIB COPYMINT ChangeLog* FAQ
%doc HACKING HELP LICENSES NEWS NOTES README* TODO
%{mint_includedir}/*
%{mint_libdir}/*


%changelog
* Mon Jun 27 2022 Dan Horák <dan[at]danny.cz> - 0.60.1-2.20140312
- little update before moving to COPR

* Wed May 14 2014 Dan Horák <dan[at]danny.cz> - 0.60.1-1.20140312
- updated to 20140312 snapshot

* Sat Oct 06 2012 Dan Horák <dan[at]danny.cz> - 0.58.0-5.20120503
- updated to 20120503 snapshot

* Sun Mar 25 2012 Dan Horák <dan[at]danny.cz> - 0.58.0-4.20111028
- updated to 20111028 snapshot
- spec cleanup

* Mon Aug 08 2011 Dan Horák <dan[at]danny.cz> - 0.58.0-3.20110725
- can be noarch

* Mon Aug 08 2011 Dan Horák <dan[at]danny.cz> - 0.58.0-2.20110725
- BR: flex-static works only on Fedora

* Mon Aug 08 2011 Dan Horák <dan[at]danny.cz> - 0.58.0-1.20110725
- initial Fedora release
