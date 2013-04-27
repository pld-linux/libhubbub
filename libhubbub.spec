#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	HTML5 compliant parsing library
Name:		libhubbub
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	625ea927b9134276d82960ab9bc03cb1
Patch0:		lib.patch
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
%patch0 -p1

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhubbub.so.*.*.*
%ghost %{_libdir}/libhubbub.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libhubbub.so
%{_includedir}/hubbub
%{_pkgconfigdir}/libhubbub.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhubbub.a
%endif
