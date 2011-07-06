Summary: SELinux binary policy manipulation library 
Name: libsepol
Version: 2.0.41
Release: 3%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Source: http://www.nsa.gov/selinux/archives/libsepol-%{version}.tgz
Patch: libsepol-rhat.patch
URL: http://www.selinuxproject.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package static
Summary: static libraries used to build policy manipulation tools
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The libsepol-static package contains the static libraries and header files
needed for developing applications that manipulate binary policies. 

%prep
%setup -q
%patch -p1 -b .rhat
# sparc64 is an -fPIC arch, so we need to fix it here
%ifarch sparc64
sed -i 's/fpic/fPIC/g' src/Makefile
%endif

%build
make clean
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_lib} 
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir} 
mkdir -p ${RPM_BUILD_ROOT}%{_includedir} 
mkdir -p ${RPM_BUILD_ROOT}%{_bindir} 
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="${RPM_BUILD_ROOT}%{_libdir}" SHLIBDIR="${RPM_BUILD_ROOT}/%{_lib}" install
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolbools
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolusers
rm -f ${RPM_BUILD_ROOT}%{_bindir}/chkcon
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%postun -p /sbin/ldconfig

%files static
%defattr(-,root,root)
%{_libdir}/libsepol.a

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol/*.h
%{_mandir}/man3/*.3.gz
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h

%files
%defattr(-,root,root)
/%{_lib}/libsepol.so.1

%changelog
* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> 2.0.41-3
- Fix libsepol.pc file
Resolves: #566496

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.41-2
- Resolve specfile problems
Resolves: #555835

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.41-1
- Upgrade to latest from NSA
  * Fixed typo in error message from Manoj Srivastava.

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> 2.0.40-1
- Upgrade to latest from NSA
  * Add pkgconfig file from Eamon Walsh.

* Tue Oct 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.39-1
- Upgrade to latest from NSA
  * Add support for building Xen policies from Paul Nuzzi.

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.38-1
- Upgrade to latest from NSA
  * Check last offset in the module package against the file size.
  Reported by Manoj Srivastava for bug filed by Max Kellermann.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> 2.0.37-1
- Upgrade to latest from NSA
  * Add method to check disable dontaudit flag from Christopher Pardy.

* Wed Mar 25 2009 Dan Walsh <dwalsh@redhat.com> 2.0.36-1
- Upgrade to latest from NSA
  * Fix boolean state smashing from Joshua Brindle.

* Thu Mar 5 2009 Dan Walsh <dwalsh@redhat.com> 2.0.35-3
- Fix license specification to be LGPL instead of GPL

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-2

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.35-1
- Upgrade to latest from NSA
        * Fix alias field in module format, caused by boundary format change
          from Caleb Case.

* Tue Oct 14 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-1
- Upgrade to latest from NSA
  * Add bounds support from KaiGai Kohei.
  * Fix invalid aliases bug from Joshua Brindle.

* Tue Sep 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.33-1
- Upgrade to latest from NSA
  * Revert patch that removed expand_rule.

* Mon Jul 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.32-1
- Upgrade to latest from NSA
  * Allow require then declare in the source policy from Joshua Brindle.

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.31-1
- Upgrade to latest from NSA
  * Fix mls_semantic_level_expand() to handle a user require w/o MLS information from Stephen Smalley.

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.30-1
- Upgrade to latest from NSA
  * Fix endianness bug in the handling of network node addresses from Stephen Smalley.
    Only affects big endian platforms.
    Bug reported by John Weeks of Sun upon policy mismatch between x86 and sparc.

* Wed May 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.29-1
- Upgrade to latest from NSA
  * Merge user and role mapping support from Joshua Brindle.

* Mon May 19 2008 Dan Walsh <dwalsh@redhat.com> 2.0.28-1
- Upgrade to latest from NSA
  * Fix mls_level_convert() to gracefully handle an empty user declaration/require from Stephen Smalley.
  * Belatedly merge test for policy downgrade from Todd Miller.

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> 2.0.26-1
- Upgrade to latest from NSA
  * Add permissive domain support from Eric Paris.

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.25-1
- Upgrade to latest from NSA
  * Drop unused ->buffer field from struct policy_file.
  * Add policy_file_init() initalizer for struct policy_file and use it, from Todd C. Miller.


* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.23-1
- Upgrade to latest from NSA
  * Accept "Flask" as an alternate identifier string in kernel policies from Stephen Smalley.
  * Add support for open_perms policy capability from Eric Paris.

* Wed Feb 20 2008 Dan Walsh <dwalsh@redhat.com> 2.0.21-1
- Upgrade to latest from NSA
  * Fix invalid memory allocation in policydb_index_others() from Jason Tang.

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> 2.0.20-1
- Upgrade to latest from NSA
  * Port of Yuichi Nakamura's tune avtab to reduce memory usage patch from the kernel avtab to libsepol from Stephen Smalley.

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.19-1
- Upgrade to latest from NSA
  * Add support for consuming avrule_blocks during expansion to reduce
    peak memory usage.

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 2.0.18-2
- Fixed for spec review

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.18-1
- Upgrade to latest from NSA
  * Added support for policy capabilities from Todd Miller.
  * Prevent generation of policy.18 with MLS enabled from Todd Miller.

* Mon Dec 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-1
- Upgrade to latest from NSA
  * print module magic number in hex on mismatch, from Todd Miller.

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.15-1
- Upgrade to latest from NSA
  * clarify and reduce neverallow error reporting from Stephen Smalley.

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-1
- Upgrade to latest from NSA
  * Reject self aliasing at link time from Stephen Smalley.
  * Allow handle_unknown in base to be overridden by semanage.conf from Stephen Smalley.
  * Fixed bug in require checking from Stephen Smalley.
  * Added user hierarchy checking from Todd Miller.  

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.11-1
  * Pass CFLAGS to CC even on link command, per Dennis Gilmore.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-1
- Upgrade to latest from NSA
  * Merged support for the handle_unknown policydb flag from Eric Paris.

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-1
- Upgrade to latest from NSA
  * Moved next_entry and put_entry out-of-line to reduce code size from Ulrich Drepper.
  * Fixed module_package_read_offsets bug introduced by the prior patch.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-1
- Upgrade to latest from NSA
  * Eliminate unaligned accesses from policy reading code from Stephen Smalley.

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-1
- Upgrade to latest from NSA
  * Allow dontaudits to be turned off during policy expansion


* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
- Upgrade to latest from NSA
     * Fix sepol_context_clone to handle a NULL context correctly.
          This happens for e.g. semanage_fcontext_set_con(sh, fcontext, NULL)
    to set the file context entry to "<<none>>".
- Apply patch from Joshua Brindle to disable dontaudit rules


* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Upgrade to latest from NSA
  * Merged error handling patch from Eamon Walsh.

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-1
- Upgrade to latest from NSA
  * Merged add boolmap argument to expand_module_avrules() from Chris PeBenito.

* Fri Mar 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Upgrade to latest from NSA
  * Merged fix from Karl to remap booleans at expand time to 
    avoid holes in the symbol table.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Upgrade to latest from NSA
  * Merged libsepol segfault fix from Stephen Smalley for when
    sensitivities are required but not present in the base.
  * Merged patch to add errcodes.h to libsepol by Karl MacMillan.
  
* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> 1.16.0-1
- Upgrade to latest from NSA
  * Updated version for stable branch.

* Tue Dec 12 2006 Adam Jackson <ajax@redhat.com> 1.15.3-1
- Add dist tag and rebuild, fixes 6 to 7 upgrades.

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Upgrade to latest from NSA
  * Merged patch to compile wit -fPIC instead of -fpic from
    Manoj Srivastava to prevent hitting the global offest table
    limit. Patch changed to include libselinux and libsemanage in
    addition to libselinux.

* Wed Nov 1 2006 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Upgrade to latest from NSA
  * Merged fix from Karl MacMillan for a segfault when linking
    non-MLS modules with users in them.

* Tue Oct 24 2006 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Upgrade to latest from NSA
  * Merged fix for version comparison that was preventing range
    transition rules from being written for a version 5 base policy
    from Darrel Goeddel.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> 1.14-1
- NSA Released version - Same as previous but changed release number

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> 1.12.28-1
- Upgrade to latest from NSA
  * Build libsepol's static object files with -fpic

* Thu Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 1.12.27-1
- Upgrade to latest from NSA
  * Merged mls user and range_transition support in modules
    from Darrel Goeddel

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.12.26-1
- Upgrade to latest from NSA
  * Merged range transition enhancements and user format changes
    Darrel Goeddel

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-3
- Fix location of include directory to devel package

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-2
- Remove invalid Requires 

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-1
- Upgrade to latest from NSA
  * Merged conditionally expand neverallows patch from Jeremy Mowery.
  * Merged refactor expander patch from Jeremy Mowery.

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 1.12.24-1
- Upgrade to latest from NSA
  * Merged libsepol unit tests from Joshua Brindle.
  * Merged symtab datum patch from Karl MacMillan.
  * Merged netfilter contexts support from Chris PeBenito.

* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 1.12.21-1
- Upgrade to latest from NSA
  * Merged helpful hierarchy check errors patch from Joshua Brindle.
  * Merged semodule_deps patch from Karl MacMillan.
    This adds source module names to the avrule decls.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.12.19-1.1
- rebuild

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.12.19-1
- Upgrade to latest from NSA
  * Lindent.
  * Merged optionals in base take 2 patch set from Joshua Brindle.

* Tue Jun 13 2006 Bill Nottingham <notting@redhat.com> 1.12.17-2
- bump so it's newer than the FC5 version

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.12.17-1
- Upgrade to latest from NSA
  * Revert 1.12.16.
  * Merged cleaner fix for bool_ids overflow from Karl MacMillan,
    replacing the prior patch.
  * Merged fixes for several memory leaks in the error paths during
    policy read from Serge Hallyn.

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.12.14-1
- Upgrade to latest from NSA
  * Fixed bool_ids overflow bug in cond_node_find and cond_copy_list,
    based on bug report and suggested fix by Cedric Roux.
  * Merged sens_copy_callback, check_role_hierarchy_callback,
    and node_from_record fixes from Serge Hallyn.

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.12.12-1
- Upgrade to latest from NSA
  * Added sepol_policydb_compat_net() interface for testing whether
    a policy requires the compatibility support for network checks
    to be enabled in the kernel.

* Thu May 15 2006 Dan Walsh <dwalsh@redhat.com> 1.12.11-1
- Upgrade to latest from NSA
  * Merged patch to initialize sym_val_to_name arrays from Kevin Carr.
    Reworked to use calloc in the first place, and converted some other
    malloc/memset pairs to calloc calls.

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 1.12.10-1
- Upgrade to latest from NSA
  * Merged patch to revert role/user decl upgrade from Karl MacMillan.

* Thu May 11 2006 Steve Grubb <sgrubb@redhat.com> 1.12.9
- Couple minor spec file clean ups

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.12.9-1
- Upgrade to latest from NSA
  * Dropped tests from all Makefile target.
  * Merged fix warnings patch from Karl MacMillan.
  * Merged libsepol test framework patch from Karl MacMillan.

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 1.12.6-1
- Upgrade to latest from NSA
  * Fixed cond_normalize to traverse the entire cond list at link time.

* Wed Apr 5 2006 Dan Walsh <dwalsh@redhat.com> 1.12.5-1
- Upgrade to latest from NSA
  * Merged fix for leak of optional package sections from Ivan Gyurdiev.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> 1.12.4-1
- Upgrade to latest from NSA
  * Generalize test for bitmap overflow in ebitmap_set_bit.

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 1.12.3-1
- Upgrade to latest from NSA
  * Fixed attr_convert_callback and expand_convert_type_set
    typemap bug.

* Fri Mar 24 2006 Dan Walsh <dwalsh@redhat.com> 1.12.2-1
- Upgrade to latest from NSA
  * Fixed avrule_block_write num_decls endian bug.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.12.1-1
- Upgrade to latest from NSA
  * Fixed sepol_module_package_write buffer overflow bug.

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.12-2
- Upgrade to latest from NSA
  * Updated version for release.
  * Merged cond_evaluate_expr fix from Serge Hallyn (IBM).
  * Fixed bug in copy_avrule_list reported by Ivan Gyurdiev.
  * Merged sepol_policydb_mls_enabled interface and error handling
    changes from Ivan Gyurdiev.

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 1.11.18-2
- Rebuild for fc5-head

* Fri Feb 17 2006 Dan Walsh <dwalsh@redhat.com> 1.11.18-1
- Upgrade to latest from NSA
  * Merged node_expand_addr bugfix and node_compare* change from
    Ivan Gyurdiev.

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 1.11.17-1
- Upgrade to latest from NSA
  * Merged nodes, ports: always prepend patch from Ivan Gyurdiev.
  * Merged bug fix patch from Ivan Gyurdiev.
  * Added a defined flag to level_datum_t for use by checkpolicy.
  * Merged nodecon support patch from Ivan Gyurdiev.
  * Merged cleanups patch from Ivan Gyurdiev.  

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.14-2
- Fix post install not to fire if /dev/initctr does not exist

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.14-1
- Upgrade to latest from NSA
  * Merged optionals in base patch from Joshua Brindle.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.11.13-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 1.11.13-1
- Upgrade to latest from NSA
  * Merged seuser/user_extra support patch from Joshua Brindle.
  * Merged fix patch from Ivan Gyurdiev.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.11.12-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.11.12-1
- Upgrade to latest from NSA
  * Merged assertion copying bugfix from Joshua Brindle.
  * Merged sepol_av_to_string patch from Joshua Brindle.
  * Merged clone record on set_con patch from Ivan Gyurdiev.  

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.11.10-1
- Upgrade to latest from NSA
  * Merged cond_expr mapping and package section count bug fixes
    from Joshua Brindle.
  * Merged improve port/fcontext API patch from Ivan Gyurdiev.  
  * Merged fixes for overflow bugs on 64-bit from Ivan Gyurdiev.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.9-1
- Upgrade to latest from NSA
  * Merged size_t -> unsigned int patch from Ivan Gyurdiev.

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.11.8-1
- Upgrade to latest from NSA
  * Merged 2nd const in APIs patch from Ivan Gyurdiev.

* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 1.11.7-1
- Upgrade to latest from NSA
  * Merged const in APIs patch from Ivan Gyurdiev.
  * Merged compare2 function patch from Ivan Gyurdiev.
  * Fixed hierarchy checker to only check allow rules.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.11.5-1
- Upgrade to latest from NSA
  * Merged further fixes from Russell Coker, specifically:
    - av_to_string overflow checking
    - sepol_context_to_string error handling
    - hierarchy checking memory leak fixes and optimizations
    - avrule_block_read variable initialization
  * Marked deprecated code in genbools and genusers.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.11.4-1
- Upgrade to latest from NSA
  * Merged bugfix for sepol_port_modify from Russell Coker.
  * Fixed bug in sepol_iface_modify error path noted by Ivan Gyurdiev.
  * Merged port ordering patch from Ivan Gyurdiev.

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.11.2-2
- Upgrade to latest from NSA
  * Merged patch series from Ivan Gyurdiev.
    This includes patches to:
    - support ordering of records in compare function
    - enable port interfaces
    - add interfaces for context validity and range checks
    - add include guards

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.11.1-2
- Add Ivans patch to make ports work

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 1.11.1-1
- Upgrade to latest from NSA
  * Fixed mls_range_cpy bug.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.9.42-1
- Upgrade to latest from NSA
  * Dropped handle from user_del_role interface.  

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.41-1
- Upgrade to latest from NSA
  * Merged remove defrole from sepol patch from Ivan Gyurdiev.

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.9.40-1
- Upgrade to latest from NSA
  * Merged module function and map file cleanup from Ivan Gyurdiev.
  * Merged MLS and genusers cleanups from Ivan Gyurdiev.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.9.39-1
- Upgrade to latest from NSA
  Prepare for removal of booleans* and *.users files.
  * Cleaned up sepol_genbools to not regenerate the image if
    there were no changes in the boolean values, including the
    degenerate case where there are no booleans or booleans.local
    files.
  * Cleaned up sepol_genusers to not warn on missing local.users.
  
* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.9.38-1
- Upgrade to latest from NSA
  * Removed sepol_port_* from libsepol.map, as the port interfaces
    are not yet stable.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.9.37-1
- Upgrade to latest from NSA
  * Merged context destroy cleanup patch from Ivan Gyurdiev.

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.36-1
- Upgrade to latest from NSA
  * Merged context_to_string interface change patch from Ivan Gyurdiev.

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.35-1
- Upgrade to latest from NSA
  * Added src/dso.h and src/*_internal.h.
    Added hidden_def for exported symbols used within libsepol.
    Added hidden for symbols that should not be exported by
    the wildcards in libsepol.map.

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.9.34-1
- Upgrade to latest from NSA
  * Merged record interface, record bugfix, and set_roles patches 
    from Ivan Gyurdiev.

* Fri Oct 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.33-1
- Upgrade to latest from NSA
  * Merged count specification change from Ivan Gyurdiev.  

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.9.32-1
- Upgrade to latest from NSA
  * Added further checking and error reporting to 
    sepol_module_package_read and _info.
  * Merged sepol handle passing, DEBUG conversion, and memory leak
    fix patches from Ivan Gyurdiev.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.9.30-1
- Upgrade to latest from NSA
  * Removed processing of system.users from sepol_genusers and
    dropped delusers logic.
  * Removed policydb_destroy from error path of policydb_read,
    since create/init/destroy/free of policydb is handled by the
    caller now.
  * Fixed sepol_module_package_read to handle a failed policydb_read
    properly.
  * Merged query/exists and count patches from Ivan Gyurdiev.
  * Merged fix for pruned types in expand code from Joshua Brindle.
  * Merged new module package format code from Joshua Brindle.


* Mon Oct 24 2005 Dan Walsh <dwalsh@redhat.com> 1.9.26-1
- Upgrade to latest from NSA
  * Merged context interface cleanup, record conversion code, 
    key passing, and bug fix patches from Ivan Gyurdiev.               

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.9.25-1
- Upgrade to latest from NSA
  * Merged users cleanup patch from Ivan Gyurdiev.
  * Merged user record memory leak fix from Ivan Gyurdiev.
  * Merged reorganize users patch from Ivan Gyurdiev.

- Need to check for /sbin/telinit

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.23-1
- Upgrade to latest from NSA
  * Added check flag to expand_module() to control assertion
    and hierarchy checking on expansion.
  * Reworked check_assertions() and hierarchy_check_constraints()
    to take handles and use callback-based error reporting.
  * Changed expand_module() to call check_assertions() and 
    hierarchy_check_constraints() prior to returning the expanded
    policy.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.21-1
- Upgrade to latest from NSA
  * Changed sepol_module_package_set_file_contexts to copy the
    file contexts data since it is internally managed.
  * Added sepol_policy_file_set_handle interface to associate
    a handle with a policy file.
  * Added handle argument to policydb_from_image/to_image.
  * Added sepol_module_package_set_file_contexts interface.
  * Dropped sepol_module_package_create_file interface.
  * Reworked policydb_read/write, policydb_from_image/to_image, 
    and sepol_module_package_read/write to use callback-based error
    reporting system rather than DEBUG.  

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.19-1
- Upgrade to latest from NSA
  * Reworked link_packages, link_modules, and expand_module to use
  callback-based error reporting system rather than error buffering.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.9.18-1
- Upgrade to latest from NSA
  * Merged conditional expression mapping fix in the module linking
  code from Joshua Brindle.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.9.17-2
- Tell init to reexec itself in post script

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.9.17-1
- Upgrade to latest from NSA
  * Hid sepol_module_package type definition, and added get interfaces.
  * Merged new callback-based error reporting system from Ivan
  Gyurdiev.
  * Merged support for require blocks inside conditionals from
  Joshua Brindle (Tresys).

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.9.14.1-1
- Upgrade to latest from NSA
  * Fixed use of policydb_from_image/to_image to ensure proper
  init of policydb.
  * Isolated policydb internal headers under <sepol/policydb/*.h>.
  These headers should only be used by users of the static libsepol.
  Created new <sepol/policydb.h> with new public types and interfaces
  for shared libsepol.
  Created new <sepol/module.h> with public types and interfaces moved
  or wrapped from old module.h, link.h, and expand.h, adjusted for
  new public types for policydb and policy_file.
  Added public interfaces to libsepol.map.
  Some implementation changes visible to users of the static libsepol:
  1) policydb_read no longer calls policydb_init.
  Caller must do so first.
  2) policydb_init no longer takes policy_type argument.
  Caller must set policy_type separately.
  3) expand_module automatically enables the global branch.  
  Caller no longer needs to do so.
  4) policydb_write uses the policy_type and policyvers from the 
  policydb itself, and sepol_set_policyvers() has been removed.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.9.12-1
- Upgrade to latest from NSA
  * Merged function renaming and static cleanup from Ivan Gyurdiev.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.9.11-1
- Upgrade to latest from NSA
  * Merged bug fix for check_assertions handling of no assertions
  from Joshua Brindle (Tresys).
  
* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.9.10-1
- Upgrade to latest from NSA
  * Merged iterate patch from Ivan Gyurdiev.
  * Merged MLS in modules patch from Joshua Brindle (Tresys).

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.8-1
- Upgrade to latest from NSA
  * Merged pointer typedef elimination patch from Ivan Gyurdiev.
  * Merged user list function, new mls functions, and bugfix patch
    from Ivan Gyurdiev.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.7-1
- Upgrade to latest from NSA
  * Merged sepol_get_num_roles fix from Karl MacMillan (Tresys).

* Fri Sep 23 2005 Dan Walsh <dwalsh@redhat.com> 1.9.6-1
- Upgrade to latest from NSA
  * Merged bug fix patches from Joshua Brindle (Tresys).

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.9.5-1
- Upgrade to latest from NSA
  * Merged boolean record and memory leak fix patches from Ivan
  Gyurdiev.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.9.4-1
- Upgrade to latest from NSA
  * Merged interface record patch from Ivan Gyurdiev.

* Thu Sep 15 2005 Dan Walsh <dwalsh@redhat.com> 1.9.3-1
- Upgrade to latest from NSA
  * Merged fix for sepol_enable/disable_debug from Ivan
  Gyurdiev.

* Mon Sep 14 2005 Dan Walsh <dwalsh@redhat.com> 1.9.1-2
- Upgrade to latest from NSA
  * Merged stddef.h patch and debug conversion patch from 
  Ivan Gyurdiev.

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.9.1-1
- Upgrade to latest from NSA
  * Fixed expand_avtab and expand_cond_av_list to keep separate
  entries with identical keys but different enabled flags.
  * Updated version for release.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.7.24-1
- Upgrade to latest from NSA
  * Fixed symtab_insert return value for duplicate declarations.
  * Merged fix for memory error in policy_module_destroy from
  Jason Tang (Tresys).

* Mon Aug 29 2005 Dan Walsh <dwalsh@redhat.com> 1.7.22-1
- Upgrade to latest from NSA
  * Merged fix for memory leak in sepol_context_to_sid from
  Jason Tang (Tresys).
  * Merged fixes for resource leaks on error paths and
    change to scope_destroy from Joshua Brindle (Tresys).

* Tue Aug 23 2005 Dan Walsh <dwalsh@redhat.com> 1.7.20-1
- Upgrade to latest from NSA
  * Merged more fixes for resource leaks on error paths 
    from Serge Hallyn (IBM).  Bugs found by Coverity. 

* Fri Aug 19 2005 Dan Walsh <dwalsh@redhat.com> 1.7.19-1
- Upgrade to latest from NSA
  * Changed to treat all type conflicts as fatal errors.
  * Merged several error handling fixes from 
    Serge Hallyn (IBM).  Bugs found by Coverity.  

* Mon Aug 15 2005 Dan Walsh <dwalsh@redhat.com> 1.7.17-1
- Upgrade to latest from NSA
  * Fixed several memory leaks found by valgrind.

* Sun Aug 14 2005 Dan Walsh <dwalsh@redhat.com> 1.7.15-1
- Upgrade to latest from NSA
  * Fixed empty list test in cond_write_av_list.  Bug found by
    Coverity, reported by Serge Hallyn (IBM).
  * Merged patch to policydb_write to check errors 
    when writing the type->attribute reverse map from
    Serge Hallyn (IBM).  Bug found by Coverity.
  * Fixed policydb_destroy to properly handle NULL type_attr_map
    or attr_type_map.

* Sat Aug 13 2005 Dan Walsh <dwalsh@redhat.com> 1.7.14-1
- Upgrade to latest from NSA
  * Fixed empty list test in cond_write_av_list.  Bug found by
    Coverity, reported by Serge Hallyn (IBM).
  * Merged patch to policydb_write to check errors 
    when writing the type->attribute reverse map from
    Serge Hallyn (IBM).  Bug found by Coverity.
  * Fixed policydb_destroy to properly handle NULL type_attr_map
    or attr_type_map.


* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.7.13-1
- Upgrade to latest from NSA
  * Improved memory use by SELinux by both reducing the avtab 
    node size and reducing the number of avtab nodes (by not
    expanding attributes in TE rules when possible).  Added
    expand_avtab and expand_cond_av_list functions for use by
    assertion checker, hierarchy checker, compatibility code,
    and dispol.  Added new inline ebitmap operators and converted
    existing users of ebitmaps to the new operators for greater 
    efficiency.
    Note:  The binary policy format version has been incremented to 
    version 20 as a result of these changes.

* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.7.12-1
- Upgrade to latest from NSA
  * Fixed bug in constraint_node_clone handling of name sets.

* Wed Aug 10 2005 Dan Walsh <dwalsh@redhat.com> 1.7.11-1
- Upgrade to latest from NSA
  * Fix range_trans_clone to map the type values properly.

* Fri Aug 5 2005 Dan Walsh <dwalsh@redhat.com> 1.7.10-1
- Upgrade to latest from NSA
  * Merged patch to move module read/write code from libsemanage
    to libsepol from Jason Tang (Tresys).

* Tue Aug 2 2005 Dan Walsh <dwalsh@redhat.com> 1.7.9-1
- Upgrade to latest from NSA
  * Enabled further compiler warning flags and fixed them.
  * Merged user, context, port records patch from Ivan Gyurdiev.
  * Merged key extract function patch from Ivan Gyurdiev.
  * Merged mls_context_to_sid bugfix from Ivan Gyurdiev.

* Wed Jul 27 2005 Dan Walsh <dwalsh@redhat.com> 1.7.6-2
- Fix MLS Free 

* Mon Jul 25 2005 Dan Walsh <dwalsh@redhat.com> 1.7.6-1
- Upgrade to latest from NSA
  * Merged context reorganization, memory leak fixes, 
    port and interface loading, replacements for genusers and
    genbools, debug traceback, and bugfix patches from Ivan Gyurdiev.
  * Merged uninitialized variable bugfix from Dan Walsh.

* Mon Jul 25 2005 Dan Walsh <dwalsh@redhat.com> 1.7.5-2
- Fix unitialized variable problem

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.7.5-1
- Upgrade to latest from NSA
  * Merged debug support, policydb conversion functions from Ivan Gyurdiev (Red Hat).
  * Removed genpolbools and genpolusers utilities.
  * Merged hierarchy check fix from Joshua Brindle (Tresys).



* Thu Jul 14 2005 Dan Walsh <dwalsh@redhat.com> 1.7.3-1
- Upgrade to latest from NSA
  * Merged header file cleanup and memory leak fix from Ivan Gyurdiev (Red Hat).
  * Merged genbools debugging message cleanup from Red Hat.

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.7-2
- Remove genpolbools and genpoluser 

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.7-1
- Upgrade to latest from NSA
  * Merged loadable module support from Tresys Technology.

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.6-1
- Upgrade to latest from NSA
  * Updated version for release.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.10-1
- Fix reset booleans warning message
- Upgrade to latest from NSA
  * License changed to LGPL v2.1, see COPYING.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.9-2
- Upgrade to latest from NSA
  * Added sepol_genbools_policydb and sepol_genusers_policydb for
    audit2why.

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.5.8-2
- export sepol_context_to_sid

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.5.8-1
- Upgrade to latest from NSA
  * Added sepol_ prefix to Flask types to avoid 
    namespace collision with libselinux.

* Fri May 13 2005 Dan Walsh <dwalsh@redhat.com> 1.5.7-1
- Upgrade to latest from NSA
  * Added sepol_compute_av_reason() for audit2why.

* Tue Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.5.6-1
- Upgrade to latest from NSA
  * Fixed bug in role hierarchy checker.

* Mon Apr 25 2005 Dan Walsh <dwalsh@redhat.com> 1.5.5-2
- Fixes found via intel compiler

* Thu Apr 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.5-1
- Update from NSA

* Tue Mar 29 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-1
- Update from NSA

* Thu Mar 24 2005 Dan Walsh <dwalsh@redhat.com> 1.5.2-2
- Handle booleans.local

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.2-1
- Update to latest from NSA
  * Added man page for sepol_check_context.
  * Added man page for sepol_genusers function.
  * Merged man pages for genpolusers and chkcon from Manoj Srivastava.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Update to latest from NSA

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.8-1
- Update to latest from NSA
        * Cleaned up error handling in sepol_genusers and sepol_genbools.

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.3.7-1
- Update to latest from NSA
  * Merged sepol_debug and fclose patch from Dan Walsh.

* Fri Feb 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.6-3
- Make sure local_files file pointer is closed
- Stop outputing error messages

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.3.6-1
- Update to latest from NSA
  * Changed sepol_genusers to also use getline and correctly handle
    EOL.
* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.3.5-1
- Update to latest from NSA
  * Merged endianness and compute_av patches from Darrel Goeddel (TCS).
  * Merged range_transition support from Darrel Goeddel (TCS).
  * Added sepol_genusers function.

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.3.2-1
- Update to latest from NSA
  * Changed relabel Makefile target to use restorecon.

* Mon Feb 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.1-1
- Update to latest from NSA
  * Merged enhanced MLS support from Darrel Goeddel (TCS).

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.2.1.1-1
- Update to latest from NSA
  * Merged build fix patch from Manoj Srivastava.

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.2.1-1
- Update to latest from NSA

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.1.1-2
- Add optargs for build

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.1.1-1
- New version from NSA

* Fri Aug 20 2004 Colin Walters <walters@redhat.com> 1.0-2
- Apply Stephen's chkcon patch

* Thu Aug 19 2004 Colin Walters <walters@redhat.com> 1.0-1
- New upstream version

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 0.4.2-1
- Newversion from upstream implementing stringcase compare

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 0.4.1-2
- ldconfig tweaks

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 0.4.1-1
- Ignore case of true/false

* Wed Aug 11 2004 Dan Walsh <dwalsh@redhat.com> 0.4.1-1
- New version from NSA

* Tue Aug 10 2004 Dan Walsh <dwalsh@redhat.com> 0.3.1-1
- Initial version
- Created by Stephen Smalley <sds@epoch.ncsc.mil> 


