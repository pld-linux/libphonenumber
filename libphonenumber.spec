# TODO: java package
#
# Conditional build:
%bcond_with	re2		# RE2 regular expressions engine (broken as of 8.12.2)
%bcond_without	static_libs	# static libraries
#
Summary:	Library to handle international phone numbers
Summary(pl.UTF-8):	Biblioteka do obsługi międzynarodowych numerów telefonów
Name:		libphonenumber
Version:	8.12.4
Release:	1
License:	Apache v2.0 with BSD parts
Group:		Libraries
#Source0Download: https://github.com/google/libphonenumber/releases/
Source0:	https://github.com/google/libphonenumber/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0157841fe5863a9d582c3cd01c96468d
Patch0:		%{name}-link.patch
URL:		https://github.com/google/libphonenumber/
BuildRequires:	boost-devel >= 1.40.0
BuildRequires:	cmake >= 2.8.5
BuildRequires:	gtest-devel
BuildRequires:	jre
BuildRequires:	libicu-devel >= 4.4
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 2.4
%{?with_re2:BuildRequires:	re2-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google's common C++ library for parsing, formatting, storing and
validating international phone numbers.

%description -l pl.UTF-8
Wspólna biblioteka C++ Google'a do analizy, formatowania,
przechowywania oraz sprawdzania poprawności międzynarodowych numerów
telefonów.

%package devel
Summary:	Header files for libphonenumber library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libphonenumber
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.40.0
Requires:	libicu-devel
Requires:	libstdc++-devel
Requires:	protobuf-devel

%description devel
Header files for libphonenumber library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libphonenumber.

%package static
Summary:	Static libphonenumber libraries
Summary(pl.UTF-8):	Statyczne biblioteki libphonenumber
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libphonenumber libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libphonenumber.

%prep
%setup -q
%patch0 -p1

%build
install -d build/cpp
cd build/cpp
%cmake ../../cpp \
	%{!?with_static_libs:-DBUILD_STATIC_LIB=OFF} \
	%{?with_re2:-DUSE_RE2=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/cpp install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS FALSEHOODS.md FAQ.md LICENSE.Chromium README.md release_notes.txt cpp/{LICENSE,README}
%attr(755,root,root) %{_libdir}/libgeocoding.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeocoding.so.8
%attr(755,root,root) %{_libdir}/libphonenumber.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libphonenumber.so.8

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeocoding.so
%attr(755,root,root) %{_libdir}/libphonenumber.so
%{_includedir}/phonenumbers

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgeocoding.a
%{_libdir}/libphonenumber.a
%endif
