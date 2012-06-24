Summary:	Cross HP Parisc GNU binary utility development utilities - gcc
Summary(es.UTF-8):   Utilitarios para desarrollo de binarios de la GNU - HP Parisc gcc
Summary(fr.UTF-8):   Utilitaires de développement binaire de GNU - HP Parisc gcc
Summary(pl.UTF-8):   Skrośne narzędzia programistyczne GNU dla HP Parisc - gcc
Summary(pt_BR.UTF-8):   Utilitários para desenvolvimento de binários da GNU - HP Parisc gcc
Summary(tr.UTF-8):   GNU geliştirme araçları - HP Parisc gcc
Name:		crosshppa-gcc
Version:	3.3.6
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	6936616a967da5a0b46f1e7424a06414
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crosshppa-binutils >= 2.15.91.0.1
BuildRequires:	flex
BuildRequires:	/bin/bash
Requires:	crosshppa-binutils >= 2.15.91.0.1
Requires:	gcc-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		hppa-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc-lib/%{target}
%define		gcclib		%{_libdir}/gcc-lib/%{target}/%{version}
%define		_noautostrip	.*%{gcclib}/libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on HP Parisc (architecture "hppa-linux")
on other machines.

%description -l de.UTF-8
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für HP Parisc zu generieren.

%description -l pl.UTF-8
Ten pakiet zawiera skrośny gcc pozwalający na tworzenie na innych
maszynach binariów do uruchamiania na HP Parisc (architektura
"hppa-linux").

%prep
%setup -q -n gcc-%{version}

%build
cp -f /usr/share/automake/config.sub .
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--includedir=%{arch}/include \
	--disable-shared \
	--disable-threads \
	--enable-languages="c" \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-x \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't want target's lib in this place
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-gcc-%{version}
%attr(755,root,root) %{_bindir}/%{target}-gccbug
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-gcc.1*
