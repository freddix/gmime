%define		apiver	2.6

Summary:	GMIME library
Name:		gmime
Version:	2.6.20
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	http://download.gnome.org/sources/gmime/2.6/%{name}-%{version}.tar.xz
# Source0-md5:	82612c42f39f6e75273a92e6de44554f
Patch0:		%{name}-link.patch
URL:		http://spruce.sourceforge.net/gmime/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gobject-introspection-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows you to manipulate MIME messages.

%package devel
Summary:	Header files to develop libgmime applications
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files develop libgmime applications.

%package apidocs
Summary:	libgmime API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libgmime API documentation.

%prep
%setup -q
%patch0 -p1

%build
cp /usr/share/gettext/config.rpath .
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-mono		\
	--disable-silent-rules	\
	--disable-static	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %ghost %{_libdir}/libgmime-*.so.?
%attr(755,root,root) %{_libdir}/libgmime-%{apiver}.so.*.*.*
%{_libdir}/girepository-1.0/GMime-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgmime-%{apiver}.so
%{_pkgconfigdir}/gmime-%{apiver}.pc
%{_includedir}/gmime-%{apiver}
%{_datadir}/gir-1.0/GMime-%{apiver}.gir
%{_datadir}/vala/vapi/*.deps
%{_datadir}/vala/vapi/*.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gmime-%{apiver}

