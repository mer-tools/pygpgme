%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:       pygpgme
Summary:    Python module for working with OpenPGP messages
Version:    0
Release:    1
Group:      Development/Languages
License:    LGPLv2+
URL:        http://cheeseshop.python.org/pypi/pygpgme/0.1
Source0:    http://cheeseshop.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  python-devel
BuildRequires:  gpgme-devel

%description
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.

%prep
%setup -q -n %{name}-%{version}

%build

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot} -O1

# No need to ship the tests
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/gpgme/tests/

%files
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/*
