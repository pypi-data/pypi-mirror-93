Summary: Utility for obtaining short-lived cookies for accessing Shibbolized SPs
Name: ecp-cookie-init
Version: 2.0.0
Release: 1%{?dist}
Source0: http://software.igwn.org/sources/source/%{name}-%{version}.tar.gz
License: GPLv3+
BuildArch: noarch
Url: https://wiki.ligo.org/AuthProject

# -- build requirements

# macros
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build
BuildRequires: python3
BuildRequires: python%{python3_pkgversion}-setuptools

# tests
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-ciecplib >= 0.4.1-2

# man pages
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-argparse-manpage
%else
BuildRequires: help2man
%endif

# -- packages

# ecp-cookie-init
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
%description
%{summary}

# python3-ecp-cookie-init
%package -n python%{python3_pkgversion}-%{name}
Summary: Python %{python3_version} modules for %{name}
Requires: python%{python3_pkgversion}-ciecplib >= 0.4.1-2
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The Python %{python3_version} modules for %{name}

# -- build

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

# for RHEL<8 generate the man page using help2man
%if 0%{?rhel} > 0 && 0%{?rhel} < 8
mkdir -p %{buildroot}%{_mandir}/man1/
env PYTHONPATH=%{buildroot}%{python3_sitelib} help2man \
	--source %{name} \
	--no-info \
	--no-discard-stderr \
	--name "generate an ECP cookie using CIECPLib" \
	--output %{buildroot}%{_mandir}/man1/ecp-cookie-init.1 \
	%{buildroot}%{_bindir}/ecp-cookie-init
%endif

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
export PATH="%{buildroot}%{_bindir}:${PATH}"
# run the unit tests
%{__python3} -m pytest --pyargs ecp_cookie_init.tests
# test basic executable functionality
ecp-cookie-init -h
ecp-cookie-init -v

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{name}
%license COPYING
%doc README.md
%{python3_sitelib}

%files
%license COPYING
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Thu Jan 28 2021 Duncan Macleod <duncan.macleod@ligo.org> - 2.0.0-1
- rewrite in python

* Thu Dec 03 2020 Satya Mohapatra <patra@mit.edu> - 1.3.7-1
- kagra access
* Wed Dec 21 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.6-1
- Add option to force Kerberos authentication by skipping klist check
- Allow target output to be redirected to a file, or not output at all
- Add options for quiet mode, and to specify cookiefile
* Mon Jun 13 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.5-1
- Use system version of Python
- Fixed for Python 3
* Wed Nov 04 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.4-1
- Use system version of curl
- Fixed bugs in Kerberos support
* Thu Oct 15 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.3-1
- Added explicit Kerberos support
- Added concurrent cookie sessions
- Added invalid password warning
- Added destroy option
* Thu Aug 27 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.2-1
- Fixed ecp-cookie-init reporting incorrect version
* Mon Jul 20 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.1-1
- Added automatic failover for LIGO IdP servers
* Wed Apr 03 2013 Peter Couvares <peter.couvares@ligo.org> - 1.1.0-1
- Fixed for MacOS.
- Added LIGO Guest and Cardiff University IdP support.
- Fixed typo in error message.
* Thu Mar 14 2013 Peter Couvares <peter.couvares@ligo.org> - 1.0.0-1
- Initial version.
