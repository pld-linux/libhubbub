#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	HTML5 compliant parsing library
Name:		libhubbub
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	625ea927b9134276d82960ab9bc03cb1
URL:		http://www.netsurf-browser.org/projects/libhubbub/
BuildRequires:	libparserutils-devel >= 0.1.2
BuildRequires:	netsurf-buildsystem
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

%package devel
Summary:	libhubbub library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhubbub
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libhubbub into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libhubbub w swoich
programach.

%package static
Summary:	libhubbub static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libhubbub
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libhubbub libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libhubbub.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}"
LDFLAGS="%{rpmldflags}"
export CFLAGS
export LDFLAGS

%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	-Iinclude -Isrc"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	-Iinclude -Isrc"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	Q=''

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	Q=''
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/hubbub
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
