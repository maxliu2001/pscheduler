#
# RPM Spec for pScheduler RPM Macros
#

%define perfsonar_auto_version 5.0.3
%define perfsonar_auto_relnum 1

Name:		pscheduler-rpm
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}

Summary:	Macros for use by pScheduler RPM specs
BuildArch:	noarch
License:	ASL 2.0
Vendor:	perfSONAR
Group:		Unspecified

Provides:	%{name} = %{version}-%{release}

%description
Macros for use by pScheduler RPM specs

# Where macros live
%define macro_dir %{_sysconfdir}/rpm
%define macro_prefix %{macro_dir}/macros.

# No punctuation between these is intentional.
%define macro_file %{macro_prefix}%{name}

%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{macro_dir}
cat > $RPM_BUILD_ROOT/%{macro_prefix}%{name} <<EOF
#
# Macros used in building pScheduler RPMs  (Version %{version})
#

%if %{?_rundir:0}%{!?_rundir:1}
# This didn't appear until EL7
%%_rundir %{_localstatedir}/run
%endif


#
# Python
#

# This is the version we like.
%%_pscheduler_python_version_major 3
%%_pscheduler_python_version_minor 6


%if 0%{?el7}
# EL7 supports 2, 34 and 36 and names its packages that way (e.g.,
# python36-foo) and has some named python3-foo.
%%_pscheduler_python python%%{_pscheduler_python_version_major}
%%_pscheduler_python_epel python%%{_pscheduler_python_version_major}%%{_pscheduler_python_version_minor}
%endif

%if 0%{?el8}
# EL7 supports Alma and Rocky.  RHEL is untested.
# See https://yum.oracle.com/oracle-linux-python.html
# EL8 standardized on just the major version, as did EPEL.
%%_pscheduler_python python%%{_pscheduler_python_version_major}
%%_pscheduler_python_epel python%%{_pscheduler_python_version_major}
%endif

%if 0%{?el9}
# EL9 has everyting as just plain python
# See https://yum.oracle.com/oracle-linux-python.html
# EL8 standardized on just the major version, as did EPEL.
%%_pscheduler_python python
%%_pscheduler_python_epel python
%endif


#
# PostgreSQL
#

# Minimum-required PostgreSQL version.  This is the one we build.
%%_pscheduler_postgresql_version_major 10
%%_pscheduler_postgresql_version_minor 17
%%_pscheduler_postgresql_version %%{_pscheduler_postgresql_version_major}.%%{_pscheduler_postgresql_version_minor}
%%_pscheduler_postgresql_data_top %%{_sharedstatedir}/pgsql
%%_pscheduler_postgresql_user postgres
%%_pscheduler_postgresql_group postgres

%if 0%{?el7}
# CentOS 7 uses the PGDG-supplied server, which has its own naming conventions.
%%_pscheduler_postgresql_package postgresql%%{_pscheduler_postgresql_version_major}
%%_pscheduler_postgresql_service postgresql-%%{_pscheduler_postgresql_version_major}
%%_pscheduler_postgresql_data %%{_pscheduler_postgresql_data_top}/%%{_pscheduler_postgresql_version_major}/data
%%_pscheduler_postgresql_initdb %%{_usr}/pgsql-%%{_pscheduler_postgresql_version_major}/bin/postgresql-%%{_pscheduler_postgresql_version_major}-setup initdb
%%_pscheduler_postgresql_plpython %%{_pscheduler_postgresql_package}-plpython%%{_pscheduler_python_version_major}
%endif

%if 0%{?el8}%{?el9}
# EL8 and EL9 keep it simple(r).
%%_pscheduler_postgresql_package postgresql
%%_pscheduler_postgresql_service postgresql
%%_pscheduler_postgresql_data %%{_pscheduler_postgresql_data_top}/data
%%_pscheduler_postgresql_initdb postgresql-setup --initdb
%%_pscheduler_postgresql_plpython %%{_pscheduler_postgresql_package}-plpython%%{_pscheduler_python_version_major}
%endif

%%_pscheduler_postgresql_version_file %%{_pscheduler_postgresql_data}/PG_VERSION


#
# pScheduler
#

%%_pscheduler_libexecdir %%{_libexecdir}/pscheduler
%%_pscheduler_sysconfdir %%{_sysconfdir}/pscheduler
%%_pscheduler_sudoersdir %%{_sysconfdir}/sudoers.d
%%_pscheduler_docdir %%{_defaultdocdir}/pscheduler
%%_pscheduler_datadir %%{_datadir}/pscheduler
%%_pscheduler_vardir %%{_var}/lib/pscheduler

# Where RPM Macros live
%%_pscheduler_rpmmacrodir %{macro_dir}
# Prefix for all macro files.  Use as %{_pscheduler_rpmmacroprefix}foo
%%_pscheduler_rpmmacroprefix %{macro_prefix}

# Internal commands
%%_pscheduler_internals %%{_pscheduler_libexecdir}/internals

# Where all classes live
%%_pscheduler_classes %%{_pscheduler_libexecdir}/classes

# Tests
%%_pscheduler_test_libexec %%{_pscheduler_classes}/test
%%_pscheduler_test_doc %%{_pscheduler_docdir}/test
%%_pscheduler_test_confdir %%{_pscheduler_sysconfdir}/test

# Tools
%%_pscheduler_tool_libexec %%{_pscheduler_classes}/tool
%%_pscheduler_tool_doc %%{_pscheduler_docdir}/tool
%%_pscheduler_tool_confdir %%{_pscheduler_sysconfdir}/tool
%%_pscheduler_tool_vardir %%{_pscheduler_vardir}/tool

# Archivers
%%_pscheduler_archiver_libexec %%{_pscheduler_classes}/archiver
%%_pscheduler_archiver_doc %%{_pscheduler_docdir}/archiver

# Context Changers
%%_pscheduler_context_libexec %%{_pscheduler_classes}/context
%%_pscheduler_context_doc %%{_pscheduler_docdir}/context

# pScheduler front-end comands
%%_pscheduler_commands %%{_pscheduler_libexecdir}/commands

# pScheduler daemons
%%_pscheduler_daemons %%{_pscheduler_libexecdir}/daemons

EOF


%files
%attr(444,root,root) %{macro_prefix}*
