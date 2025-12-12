%define module pdbpp
%bcond_without test

Name:		python-pdbpp
Version:	0.10.3
Release:	2
Summary:	PDB++, a drop-in replacement for pdb
URL:		https://github.com/pdbpp/pdbpp
License:	BSD-3-Clause
Group:		Development/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pdbpp/pdbpp-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch

BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	python%{pyver}dist(wmctrl)
BuildRequires:	python%{pyver}dist(fancycompleter)
BuildRequires:	python%{pyver}dist(pdm-backend)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
%if %{with test}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	ipython
%endif


%description
PDB++, a drop-in replacement for pdb.

%prep
%autosetup -p1 -n %{module}-%{version}

%build
%py_build

%install
%py3_install

%if %{with test}
%check
pytest -v testing/ -k "not test_completes_from_pdb and not test_python_m_pdb_uses_pdbpp and not test_pdbrc_continue"
%endif

%files
%{py_sitedir}/_pdbpp_path_hack
%{py_sitedir}/pdb.py
%{py_sitedir}/%{module}*.pth
%{py_sitedir}/%{module}-%{version}*.*-info
%license LICENSE.txt
%doc README.rst