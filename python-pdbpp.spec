%define module pdbpp
%bcond_without test

Name:		python-pdbpp
Version:	0.12.0
Release:	1
Summary:	PDB++, a drop-in replacement for pdb
# Upstream was forked to continue package maintenance, this is the new upstream URL
URL:		https://github.com/bretello/pdbpp
License:	BSD-3-Clause
Group:		Development/Python
Source0:	https://github.com/bretello/pdbpp/archive/%{version}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	python%{pyver}dist(wmctrl)
BuildRequires:	python%{pyver}dist(fancycompleter)
BuildRequires:	python%{pyver}dist(pdm-backend)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with test}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-asyncio)
BuildRequires:	python%{pyver}dist(ipython)
BuildRequires:	python%{pyver}dist(pexpect)
BuildRequires:	python%{pyver}dist(pyrepl)
BuildRequires:	python%{pyver}dist(async-timeout)
%endif

%description
PDB++, a drop-in replacement for pdb.

%prep -a
# remove pytest coverage flags
sed -i '/^addopts/d' pyproject.toml

%build -p
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}

%if %{with test}
%check
# somne of these tests want read/write access in CI, some are flaky.
skiptests="not test_integration[_pyrepl] and not test_integration[readline] and not test_ipython"
skiptests+=" and not test_question_mark_unit and not test_nested_completer"
skiptests+=" and not test_set_trace_in_skipped_module and not test_exception_info_main"
skiptests+=" and not test_complete_displays_errors[False] and not test_complete_displays_errors[True]"
# deselect flaky tests
# not test_completes_from_pdb and not test_python_m_pdb_uses_pdbpp and not test_pdbrc_continue and
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest -v -k "$skiptests"
%endif

%files
%{py_sitedir}/_pdbpp_path_hack
%{py_sitedir}/__pycache__
%{py_sitedir}/%{module}.py
%{py_sitedir}/%{module}*.pth
%{py_sitedir}/%{module}_utils
%{py_sitedir}/%{module}-%{version}.dist-info
%license LICENSE.txt
%doc README.rst
