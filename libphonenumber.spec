# TODO: java package
#
# Conditional build:
%bcond_with	re2		# RE2 regular expressions engine (broken as of 8.12.2)
%bcond_without	static_libs	# static libraries
#
Summary:	Library to handle international phone numbers
Summary(pl.UTF-8):	Biblioteka do obsługi międzynarodowych numerów telefonów
Name:		libphonenumber
# when upgrading, check if new version contains
# tools/java/cpp-build/target/cpp-build-1.0-SNAPSHOT-jar-with-dependencies.jar (or similar)
# some releases don't contain that file and requires building it by maven
Version:	8.13.52
Release:	2
License:	Apache v2.0 with BSD parts
Group:		Libraries
#Source0Download: https://github.com/google/libphonenumber/releases/
Source0:	https://github.com/google/libphonenumber/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3d3c2ecda1372bdd05355085cc937d35
Patch0:		%{name}-link.patch
Patch1:		%{name}-no-fetch.patch
Patch2:		no-static.patch
URL:		https://github.com/google/libphonenumber/
BuildRequires:	abseil-cpp-devel
BuildRequires:	boost-devel >= 1.40.0
BuildRequires:	cmake >= 3.11
BuildRequires:	gtest-devel
BuildRequires:	jre
BuildRequires:	libicu-devel >= 4.4
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel >= 2.4
%{?with_re2:BuildRequires:	re2-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
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
Requires:	abseil-cpp-devel
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
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
install -d build/cpp
cd build/cpp
%cmake ../../cpp \
	%{!?with_static_libs:-DBUILD_STATIC_LIB=OFF} \
	-DCMAKE_CXX_STANDARD=17 \
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
%{_libdir}/cmake/libphonenumber

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgeocoding.a
%{_libdir}/libphonenumber.a
%endif
