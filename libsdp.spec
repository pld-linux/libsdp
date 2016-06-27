Summary:	User level socket switch for seamless migration to SDP
Summary(pl.UTF-8):	Przełącznik gniazd na poziomie użytkownika do przezroczystej migracji na SDP
Name:		libsdp
# 1.1.107 release is broken (undefined __sdp_sockaddr_to_sdp symbol)
Version:	1.1.108
%define	snap	20110515
%define	subver	0.17
%define	gitref	ga6958ef
Release:	%{subver}.%{snap}.1
License:	BSD or GPL v2
Group:		Libraries
Source0:	https://www.openfabrics.org/downloads/libsdp/%{name}-%{version}-%{subver}.%{gitref}.tar.gz
# Source0-md5:	badedec1a5f310247e22fb686ddaeb67
URL:		http://openib.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
libsdp is a LD_PRELOAD-able library that can be used to migrate
existing applications use InfiniBand Sockets Direct Protocol (SDP)
instead of TCP sockets, transparently and without recompilations.

%description -l pl.UTF-8
libsdp to ładowana przez LD_PRELOAD biblioteka, którą można
wykorzystać przy migrowaniu istniejących aplikacji, aby używały
protokołu InfiniBand SDP (Sockets Direct Protocol) zamiast gniazd
TCP - w sposób przezroczysty, bez rekompilacji.

%package devel
Summary:	Header file with SDP sockets definitions
Summary(pl.UTF-8):	Plik nagłówkowy z definicjami gniazd SDP
Group:		Development/Libraries
Requires:	linux-libc-headers

%description devel
Header file with SDP sockets definitions.

%description devel -l pl.UTF-8
Plik nagłówkowy z definicjami gniazd SDP.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# let's LD_PRELOAD by soname
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsdp*.{so,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libsdp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsdp.so.1
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/libsdp_sys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsdp_sys.so.1
%endif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libsdp.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/sdp_inet.h
