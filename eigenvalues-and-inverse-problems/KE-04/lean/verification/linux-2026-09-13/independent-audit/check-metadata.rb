# encoding: UTF-8
require 'yaml'; require 'json'; require 'digest'; require 'pathname'
root=Pathname('/tmp/nla-lean-ke04-worktree/eigenvalues-and-inverse-problems/KE-04/lean')
meta=YAML.load_file(root+'formalization.yaml')
manifest=JSON.parse((root+'lake-manifest.json').read)
pkgs=manifest['packages'].to_h{|x| [x['name'],x['rev']]}
pins=meta.dig('toolchain','dependencies')
checks={}
pins.each{|k,v| checks[k]={ 'metadata'=>v, 'manifest'=>pkgs[k], 'match'=>(k=='importGraph' ? pkgs[k]==v : pkgs[k]==v) }}
raw=(root+'formalization.yaml').read.force_encoding('UTF-8')
checks['_author_name']=raw.include?('George Stepaniants')
checks['_affiliation']= ['Department of Computing and Mathematical Sciences','California Institute of Technology','Pasadena','California','USA'].all?{|x| raw.include?(x)}
checks['_no_email']=raw !~ /\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b/i
checks['_default_solution']=(root+'lakefile.toml').read.include?('defaultTargets = ["Solution"]')
checks['_solution_import_proof']=((root+'Solution.lean').read.strip=='import NLA.KE04.Proof')
checks['_pending_status']=(meta.dig('status','whole_problem_verified')==false && meta.dig('status','actual_linux_comparator')=='pending' && meta.dig('status','independent_packaging_approval')=='pending')
puts JSON.pretty_generate({'pins'=>checks,'all_pins_match'=>checks.reject{|k,_| k.start_with?('_')}.values.all?{|x| x['match']},'author_and_controls'=>checks.select{|k,_| k.start_with?('_')},'main_result_count'=>meta.dig('status','main_results').length})
