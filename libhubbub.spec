#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	HTML5 compliant parsing library
Summary(pl.UTF-8):	Biblioteka analizująca HTML5
Name:		libhubbub
Version:	0.3.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	bbd91ce8fd338d9b35ac93e053f428f9
URL:		http://www.netsurf-browser.org/projects/libhubbub/
BuildRequires:	libparserutils-devel >= 0.2.4
BuildRequires:	netsurf-buildsystem >= 1.7
Requires:	libparserutils >= 0.2.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hubbub is an HTML5 compliant parsing library, written in C. It was
developed as part of the NetSurf project and is available for use by
other software under the MIT licence.

The HTML5 specification defines a parsing algorithm, based on the
behaviour of mainstream browsers, which provides instructions for how
to parse all markup, both valid and invalid. As a result, Hubbub
parses web content well.

If you are looking for an HTML5 parser in Python or Ruby, you may wish
to look at html5lib.

Features:
- Parses HTML, good and bad
- Simple C API
- Fast
- Character encoding detection
- Well-tested (~90% test coverage)
- Portable
- Shared library

%description -l pl.UTF-8
Hubbub to napisana w C biblioteka analizująca HTML5. Powstała jako
część projektu NetSurf i można jej używać w innych programach na
licencji MIT.

Specyfikacja HTML definiuje algorytm analizy w oparciu o zachowanie
głównych przeglądarek, które dostarczają instrukcje, jak analizować
znaczniki, zarówno poprawne, jak i niepoprawne. W efekcie Hubbub
dobrze analizuje treści WWW.

W razie potrzeby analizowania HTML5 w języku Python lub Ruby, można
rozważyć użycie html5lib.

Cechy biblioteki:
- analizuje HTML, dobry i wadliwy
- proste API dla języka C
- szybka
- wykrywanie kodowania znaków
- dobrze przetestowana (~90% pokrycia testami)
- przenośna
- współdzielona

%package devel
Summary:	libhubbub library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhubbub
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libparserutils-devel >= 0.2.1

%description devel
This package contains the include files and other resources you can
use to incorporate libhubbub into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libhubbub w swoich
programach.

%package static
Summary:	libhubbub static library
Summary(pl.UTF-8):	Statyczna biblioteka libhubbub
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libhubbub library.

%description static -l pl.UTF-8
Statyczna biblioteka libhubbub.

%prep
%setup -q

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libhubbub.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhubbub.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhubbub.so
%{_includedir}/hubbub
%{_pkgconfigdir}/libhubbub.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhubbub.a
%endif
