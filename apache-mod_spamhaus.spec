#Module-Specific definitions
%define mod_name mod_spamhaus
%define mod_conf B46_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache DNSBL module
Name:		apache-%{mod_name}
Version:	0.5
Release: 	%mkrel 1
Group:		System/Servers
License:	GPLv3
URL:		http://sourceforge.net/projects/mod-spamhaus/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/mod-spamhaus/%{mod_name}05.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_spamhaus is an Apache module that use DNSBL in order to block spam relay
via web forms, preventing URL injection, block http DDoS attacks from bots and
generally protecting your web service denying access to a known bad IP address.

%prep

%setup -q -n mod-spamhaus

cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c src/%{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 src/.libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ReadMe.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

