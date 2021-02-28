#
# Conditional build:
%bcond_without	static_libs		# static libraries

Summary:	SPICE Client controller library
Summary(pl.UTF-8):	Biblioteka kontrolera klienta SPICE
Name:		spice-controller
Version:	0.34
Release:	1
License:	LGPL v2.1+
Group:		X11/Applications
Source0:	https://www.spice-space.org/download/gtk/spice-gtk-%{version}.tar.bz2
# Source0-md5:	ec01b0b50337aa23f0566423b2f83109
Patch0:		%{name}-am.patch
Patch1:		%{name}-no-tunnel.patch
Patch2:		%{name}-proto-headers.patch
URL:		https://spice-space.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	celt051-devel >= 0.5.1.1
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	gcc >= 5:3.0
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 0.9.4
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libjpeg-devel
BuildRequires:	libsoup-devel >= 2.50
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	lz4-devel
BuildRequires:	openssl-devel >= 1.0.0
BuildRequires:	opus-devel >= 0.9.14
BuildRequires:	pixman-devel >= 0.17.7
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	sed >= 4.0
BuildRequires:	spice-protocol >= 0.12.11
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.36
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SPICE Client controller library.

%description -l pl.UTF-8
Biblioteka kontrolera klienta SPICE.

%package devel
Summary:	Header files for SPICE Client contoller library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienckiej SPICE controller
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36

%description devel
Header files for SPICE Client controller library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienckiej SPICE controller.

%package static
Summary:	Static SPICE controller library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka SPICE controller
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SPICE Client controller library.

%description static -l pl.UTF-8
Statyczna biblioteka kliencka SPICE controller.

%package -n vala-spice-controller
Summary:	Vala API for SPICE controller protocol headers
Summary(pl.UTF-8):	Interfejs języka Vala do nagłówków protokołu kontrolera SPICE
# there was mistaken vala-spice-protocol 0.35 through 0.38 containing spice-client-glib and spice-client-gtk APIs
Group:		Development/Libraries
Requires:	spice-controller-devel = %{version}-%{release}
Requires:	spice-protocol >= 0.12.11
Requires:	vala >= 2:0.14
# old name of vala-spice-protocol
Obsoletes:	vala-spice-gtk < 0.7
# vapi name is "spice-protocol", but it actually refers only to controller parts (controller_prot, foreign_menu_prot)
Obsoletes:	vala-spice-protocol < 0.35
BuildArch:	noarch

%description -n vala-spice-controller
Vala API for SPICE controller protocol headers.

%description -n vala-spice-controller -l pl.UTF-8
Interfejs języka Vala do nagłówków protokołu kontrolera SPICE.

%prep
%setup -q -n spice-gtk-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd spice-common
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
# smartcard,usbredir,webdav options don't affect controller library
%configure \
	--disable-gtk-doc \
	--enable-lz4 \
	--disable-silent-rules \
	--disable-smartcard \
	%{?with_static_libs:--enable-static} \
	--disable-usbredir \
	--disable-webdav \
	--without-gtk \
	--with-html-dir=%{_gtkdocdir} \
	--with-pnp-ids-path=/lib/hwdata/pnp.ids \
	--with-usb-ids-path=/lib/hwdata/usb.ids
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%{__rm} $RPM_BUILD_ROOT%{_bindir}/* \
	$RPM_BUILD_ROOT%{_mandir}/man1/* \
	$RPM_BUILD_ROOT%{_localedir}/*/LC_MESSAGES/spice-gtk.mo
%{__rm} -r $RPM_BUILD_ROOT%{_gtkdocdir}/spice-gtk

# libspice-client-glib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspice-client-glib-2.0.* \
	$RPM_BUILD_ROOT%{_libdir}/girepository-1.0/SpiceClientGLib-2.0.typelib \
	$RPM_BUILD_ROOT%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/spice-client-glib-2.0.pc
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/spice-client-glib-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libspice-controller.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspice-controller.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspice-controller.so
%{_includedir}/spice-controller
%{_pkgconfigdir}/spice-controller.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspice-controller.a
%endif

%files -n vala-spice-controller
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/spice-protocol.vapi
