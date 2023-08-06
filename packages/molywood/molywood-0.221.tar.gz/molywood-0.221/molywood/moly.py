import sys
from glob import glob
from subprocess import call, PIPE, Popen, check_output
from shutil import which
import os
import warnings
from collections import OrderedDict

if __name__ == "__main__":
    try:
        import tcl_actions
        import graphics_actions
    except ImportError:
        import molywood.tcl_actions as tcl_actions
        import molywood.graphics_actions as graphics_actions
else:
    import molywood.tcl_actions as tcl_actions
    import molywood.graphics_actions as graphics_actions


class Script:
    """
    Main class that will combine all information
    and render the movie (possibly with multiple
    panels, overlays etc.)
    """
    allowed_globals = ['global', 'layout', 'master_overlay']
    allowed_params = {'global': ['fps', 'keepframes', 'draft', 'name', 'render', 'restart', 'breakpoints', 'gif'],
                      'layout': ['columns', 'rows'],
                      'master_overlay': ['figure', 't', 'origin', 'relative_size', 'dataframes', 'dataframes_from_file',
                                         'aspect_ratio', 'datafile', '2D', 'text', 'textsize', 'sigmoid',
                                         'alpha', 'scene', 'transparent_background', 'textcolor', 'decimal_points',
                                         'movie', 'from', 'length', 'seaborn', 'start_time', 'textbox', 'center',
                                         'angle'],
                      '_default': ['visualization', 'structure', 'trajectory', 'position', 'resolution', 'pdb_code',
                                   'after', 'contour', 'ambient_occlusion', 'draft', 'max_transparent_surfaces']}
    
    def __init__(self, scriptfile=None, log=False):
        self.name = 'movie'
        self.scenes = []
        self.directives = {}
        self.audio = []
        self.breakpoints = []
        self.master_overlays = []
        self.fps = 20
        self.log = log
        self.draft, self.do_render, self.keepframes, self.restart, self.gif = False, True, False, False, ''
        self.scriptfile = scriptfile
        self.vmd, self.compose, self.convert, self.conda, self.ffmpeg = 5 * [None]
        self.tachyon = None
        self.setup_os_commands()
        if self.scriptfile:
            self.from_file()

    def render(self):
        """
        The final fn that renders the movie (runs
        the TCL script, then uses combine and/or
        ffmpeg to assemble the movie frame by frame)
        :return: None
        """
        def render_scene(script_and_scene):  # the part below controls TCL/VMD rendering
            """
            This fn encapsulates the whole scene-rendering protocol
            :param script_and_scene: tuple, contains one Script and one Scene instance
            :return: None
            """
            script, scn = script_and_scene
            print("Now rendering scene: {}".format(scn.alias))
            tcl_script = scn.tcl()  # this generates the TCL code, below we save it as script and run VMD
            if scn.run_vmd:
                with open('script_{}.tcl'.format(scn.alias), 'w') as out:
                    out.write(tcl_script)
                ddev = '-dispdev none' if not scn.draft else ''
                if not script.do_render and not scn.draft:
                    raise RuntimeError("render=false is only compatible with draft=true")
                with open('just_an_empty_file.vmd', 'w') as out:
                    out.write('')
                if os.name == 'posix':
                    show_in_terminal = ["selections must have", "ERROR"]
                    greps = '\|'.join(show_in_terminal)
                    call_moly('{vmd} {ddev} -e script_{al}.tcl -startup just_an_empty_file.vmd 2>&1 | tee '
                              '{al}_vmdlog.moly | grep "[05].dat\|{g}"'.format(vmd=script.vmd, ddev=ddev, al=scn.alias,
                                                                               g=greps), log=self.log)
                else:
                    call_moly('{} {} -e script_{}.tcl -startup just_an_empty_file.vmd '
                              '2>&1'.format(script.vmd, ddev, scn.alias), log=self.log)
                os.remove('just_an_empty_file.vmd')
                if script.do_render:
                    for f in glob('{}-*tga'.format(scn.name)):
                        call_moly('{} {} {}'.format(script.convert, f, f.replace('tga', 'png')), log=self.log)
                        os.remove(f)
                if not scn.draft:
                    _ = [os.remove(f) for f in glob('{}-[0-9]*dat'.format(scn.name))]
            for action in scn.actions:
                action.generate_graph()  # here we generate matplotlib figs on-the-fly

        for scene in self.scenes:
            render_scene((self, scene))
        # at this stage, each scene should have all its initial frames rendered
        if self.do_render:
            graphics_actions.postprocessor(self)
            graphics_actions.add_master_overlays(self)
            call_moly('{ff} -y -framerate {fps} -i {n}-%d.png -profile:v high -crf 20 -pix_fmt yuv420p '
                      '-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {n}.mp4 > {n}_ffmpeglog.moly '
                      '2>&1'.format(fps=self.fps, n=self.name, ff=self.ffmpeg), log=self.log)
            if self.audio:
                print("Processing audio files...")
                total_frames = len([x for x in os.listdir('.') if x.startswith('{}-'.format(self.name))
                                    and x.endswith('png')])
                self.parse_audio(float(total_frames)/self.fps)
                call_moly('{ff} -y -i {n}.mp4 -i {n}_audio.mp3 -c copy -map 0:v:0 -map 1:a:0 tmp.mp4 >> '
                          '{n}_ffmpeglog.moly 2>&1'.format(n=self.name, ff=self.ffmpeg), log=self.log)
                os.rename('tmp.mp4', '{n}.mp4'.format(n=self.name))
                os.remove('{n}_audio.mp3'.format(n=self.name))
        if self.breakpoints:
            self.breakpoints = [0] + self.breakpoints
            for n in range(len(self.breakpoints)):
                try:
                    startpoint = self.breakpoints[n]
                    duration = self.breakpoints[n+1] - self.breakpoints[n]
                    call_moly('{ff} -y -i {n}.mp4 -ss {sp} -t {dur} {n}-part{q}.mp4 >> {n}_ffmpeglog.moly '
                              '2>&1'.format(n=self.name, ff=self.ffmpeg, sp=startpoint, dur=duration, q=n+1),
                              log=self.log)
                except IndexError:
                    startpoint = self.breakpoints[-1]
                    call_moly('{ff} -y -i {n}.mp4 -ss {sp} {n}-part{q}.mp4 >> {n}_ffmpeglog.moly '
                              '2>&1'.format(n=self.name, ff=self.ffmpeg, sp=startpoint, q=n+1), log=self.log)
        if self.gif:
            self.convert_to_gif()
        if not self.keepframes:
            for sc in self.scenes:
                if '/' in sc.name or '\\' in sc.name or '~' in sc.name:
                    raise RuntimeError('For security reasons, cleanup of scenes that contain path-like elements '
                                       '(slashes, backslashes, tildes) is prohibited.\n\n'
                                       'Error triggered by: {}'.format(sc.name))
                else:
                    if any([x for x in os.listdir('.') if x.startswith(sc.name) and x.endswith('png')]):
                        _ = [os.remove(f) for f in glob('{}-[0-9]*.png'.format(sc.name))]
                    if any([x for x in os.listdir('.') if x.startswith('overlay') and x.endswith('png')
                            and sc.name in x]):
                        _ = [os.remove(f) for f in glob('overlay[0-9_]*-{}-[0-9]*.png'.format(sc.name))]
                    if any([x for x in os.listdir('.') if x.startswith('script') and x.endswith('tcl')
                            and sc.name in x]):
                        _ = [os.remove(f) for f in glob('script_{}.tcl'.format(sc.name))]
            _ = [os.remove(f) for f in glob('overlay[0-9_]*-master_overlay_scene_*-[0-9]*.png'.format(sc.name))]
            if '/' in self.name or '\\' in self.name or '~' in self.name:
                raise RuntimeError('For security reasons, cleanup of scenes that contain path-like elements '
                                   '(slashes, backslashes, tildes) is prohibited.\n\n'
                                   'Error triggered by: {}'.format(self.name))
            else:
                if any([x for x in os.listdir('.') if x.startswith(self.name) and x.endswith('png')]):
                    _ = [os.remove(f) for f in glob('{}-[0-9]*.png'.format(self.name))]
    
    def show_script(self):
        """
        Shows a sequence of scenes currently
        buffered in the object for rendering;
        mostly for debugging purposes
        :return: None
        """
        for subscript in self.scenes:
            print('\n\n\tScene {}: \n\n'.format(subscript.name))
            subscript.show_script()

    def from_file(self):
        """
        Reads the full movie script from an input file
        and runs parser/setter functions
        :return: None
        """
        script = [line.strip() for line in open(self.scriptfile, 'r')]
        current_subs = ['_default']
        subscripts = OrderedDict({current_subs[0]: []})
        multiline = None
        master_setup = []
        for line in script:
            excl = line.find('!')
            if excl >= 0 and not Action.within_quotes(line, excl):
                line = line[:excl].strip()
            if line.startswith('#'):  # beginning of a subscript
                current_subs = [sub.strip() for sub in line.strip('#').strip().split(',')]
                for sub in current_subs:
                    if sub not in subscripts.keys():
                        subscripts[sub] = []
            elif line.startswith('$'):  # global directives
                master_setup.append(line.strip('$').strip())
            elif line:  # regular content of subscript
                if line.startswith('{'):  # with a possibility of multi-actions wrapped into curly brackets
                    if multiline:
                        raise RuntimeError("Action {} starts before a previous multi-action is terminated".format(line))
                    multiline = ' ' + line
                if multiline and line.strip().endswith('}'):
                    if not line.startswith('{'):
                        multiline += ' ' + line
                    for act in multiline.strip('\{\} ').split(';'):
                        if not all(len(x.split('=')) >= 2 for x in Action.split_input_line(act)[1:]):
                            raise RuntimeError("Have you forgotten to add a semicolon in action: \n\n{}?\n".format(act))
                    for sub in current_subs:  # TODO if more than 1 '=', check if others are in quot marks
                        subscripts[sub].append(multiline)
                    multiline = None
                if multiline and not line.strip().endswith('}') and not line.startswith('{'):
                    multiline += ' ' + line
                if not multiline and not line.startswith('{') and not line.endswith('}'):
                    for sub in current_subs:
                        subscripts[sub].append(line)
        if multiline:
            raise RuntimeError("Error: not all curly brackets {} were closed, revise your input")
        Script.allowed_globals.extend(list(subscripts.keys()))
        for sc in subscripts.keys():
            Script.allowed_params[sc] = Script.allowed_params['_default']
        self.directives = self.parse_directives(master_setup)
        self.scenes = self.parse_scenes(subscripts)
        self.prepare()
    
    def setup_os_commands(self):
        """
        Paths to VMD, imagemagick utilities, OS-specific
        versions of rm/del, ls/dir, which/where, ffmpeg etc.
        have to be determined to allow for Linux/OSX/Win
        compatibility. NOTE: compatibility with Windows might be
        a future feature, currently not well-tested
        :return: None
        """
        if os.name == 'posix':
            self.vmd = 'vmd'
            self.ffmpeg = 'ffmpeg'
            self.conda = 'conda'
            self.compose, self.convert = 'composite', 'convert'
        elif os.name == 'nt':
            self.ffmpeg = 'ffmpeg.exe'
            self.vmd = 'vmd.exe'
            self.conda = 'conda.exe'
            self.compose, self.convert = 'magick composite', 'magick convert'
        else:
            raise RuntimeError('OS type could not be detected')
        missing_deps, _ = check_deps()
        if missing_deps:
            if len(missing_deps) == 1 and 'seaborn' in missing_deps:
                requires_seaborn = False  # sns updates can have their moods but seaborn isn't even needed 99% of time
                for sc in self.scenes:
                    for ac in sc.actions:
                        try:
                            ovls = [ac.overlays[x] for x in ac.overlays.keys()]
                        except AttributeError:
                            pass
                        else:
                            if any(['seaborn' in ovl for ovl in ovls]):
                                requires_seaborn = True
                if not requires_seaborn:
                    return 
            conda_present = True if which(self.conda) else True
            genenv_present = 'molywood' in os.popen("{} info --envs".format(self.conda)).read()
            if os.name == 'posix':
                if conda_present and genenv_present:
                    print("\n\n *** Please type 'source activate molywood'\n\n (or 'conda activate molywood', depending"
                          " on your conda setup) \n\n to activate the virtual environment. ***")
                    sys.exit(1)
                if conda_present and not genenv_present:
                    print("\n\n *** Missing dependencies were found. To batch-install all of them, simply run "
                          "\n\n\t'molywood-gen-env'\n\n (provided that molywood was installed via pip), and then type "
                          "\n\n\t'source activate molywood'\n\n (or 'conda activate molywood', depending on your conda "
                          "setup) to activate the virtual environment. ***\n\n")
                    sys.exit(1)
                if not conda_present and not any([x in missing_deps for x in ['vmd', 'ffmpeg', 'magick']]):
                    print("\n\n *** Missing dependencies were found. To batch-install all of them, simply run "
                          "\n\n\t'molywood-gen-env'\n\n (provided that molywood was installed via pip) ***\n\n")
                    sys.exit(1)
                if not conda_present and any([x in missing_deps for x in ['vmd', 'ffmpeg', 'magick']]):
                    print("\n\n *** Missing dependencies were found. *** \n\n To batch-install them, either:\n\n"
                          " (1) install Anaconda, and then run 'molywood-gen-env';\n\n (2) install manually "
                          "the following dependencies:\n\n")
                    manual_install()
                    sys.exit(1)
            else:
                print("\n\n *** Missing dependencies were found. *** \n\n To run Molywood, please install:\n")
                manual_install()
                sys.exit(1)

    def parse_directives(self, directives):
        """
        Reads global directives that affect
        the main object (layout, fps, draftmode
        etc.) based on $-prefixed entries
        :param directives:
        :return: dict, contains dictionaries of global keyword:value parameters
        """
        dirs = OrderedDict()
        mvol_count = 0
        for directive in directives:
            entries = Action.split_input_line(directive)
            if entries[0] not in Script.allowed_globals:
                raise RuntimeError("'{}' is not an allowed global directive. Allowed "
                                   "global directives are: {}".format(entries[0], ", ".join(Script.allowed_globals)))
            dirname = entries[0]
            if entries[0] == 'master_overlay':
                entries[0] = entries[0] + str(mvol_count)
                mvol_count += 1
            if dirname.startswith('master_overlay'):
                dirs[entries[0]] = directive
            else:
                dirs[entries[0]] = OrderedDict()
                for entry in entries[1:]:
                    try:
                        key, value = entry.split('=')
                    except ValueError:
                        raise RuntimeError("Entries should contain parameters formatted as 'key=value' pairs, '{}' in"
                                           " line '{}' does not follow that specification".format(entry, directive))
                    else:
                        allowed = Script.allowed_params[dirname]
                        if key not in allowed:
                            raise RuntimeError("'{}' is not a parameter compatible with the directive {}. Allowed "
                                               "parameters include: {}".format(key, dirname,
                                                                               ", ".join(list(allowed))))
                        if len(entry.split('=')) > 2:  # master_overlay can have '=' chars in the 'text' param
                            value = '='.join(entry.split('=')[1:])
                        dirs[entries[0]][key] = value
        return dirs
    
    def parse_scenes(self, scenes):
        """
        Reads info on individual scenes and initializes
        Scene objects, later to be appended to the Script's
        list of Scenes
        :param scenes: dict, contains scene_name: description bindings
        :return: list, container of Scene objects
        """
        scenelist = []
        for sub in scenes.keys():
            if scenes[sub]:
                if sub in self.directives.keys():
                    pos, res, tcl, struct_list, traj_list, contour, ao = [1, 1], [1000, 1000], None, [], [], None, False
                    try:
                        tcl = self.directives[sub]['visualization']
                    except KeyError:
                        pass
                    else:
                        tcl = self.check_path(tcl)
                        tcl = self.check_tcl(tcl)
                    try:
                        pos = [int(x) for x in self.directives[sub]['position'].split(',')]
                    except KeyError:
                        pass
                    try:
                        res = [int(x) for x in self.directives[sub]['resolution'].split(',')]
                    except KeyError:
                        pass
                    try:
                        contour = True if self.directives[sub]['contour'].lower() in ['t', 'y', 'true', 'yes'] else None
                    except KeyError:
                        pass
                    try:
                        ao = True if self.directives[sub]['ambient_occlusion'].lower() in ['t', 'y', 'true', 'yes'] \
                            else False
                    except KeyError:
                        pass
                    try:
                        max_trans_surf = self.directives[sub]['max_transparent_surfaces']
                    except KeyError:
                        max_trans_surf = 3
                    else:
                        max_trans_surf = int(max_trans_surf)
                    try:
                        struct_list = self.directives[sub]['structure'].split(',')
                    except KeyError:
                        try:
                            pdb_list = self.directives[sub]['pdb_code'].split(',')
                        except KeyError:
                            pass
                        else:
                            for pdb in pdb_list:
                                pdb = pdb.upper()
                                if not pdb.upper() + '.pdb' in os.listdir('.'):
                                    from urllib.request import urlopen
                                    try:
                                        data = urlopen('https://files.rcsb.org/download/{}.pdb'.format(pdb)).read()
                                        data = data.decode()
                                    except:
                                        try:
                                            os.environ['PYTHONHTTPSVERIFY'] = '0'
                                            data = urlopen('https://files.rcsb.org/download/{}.pdb'.format(pdb)).read()
                                            data = data.decode()
                                        except:
                                            raise RuntimeError("Download failed, check the PDB code and your "
                                                               "connection, as well as SSL certificate settings")
                                        else:
                                            with open('{}.pdb'.format(pdb), 'w') as pdbfile:
                                                pdbfile.write(data)
                                    else:
                                        with open('{}.pdb'.format(pdb), 'w') as pdbfile:
                                            pdbfile.write(data)
                                struct_list.append('{}.pdb'.format(pdb))
                    else:
                        struct_list = [self.check_path(struct) for struct in struct_list]
                    try:
                        traj_list = self.directives[sub]['trajectory'].split(',')
                    except KeyError:
                        pass
                    else:
                        traj_list = [self.check_path(traj) for traj in traj_list]
                    try:
                        dft = self.directives[sub]['draft']
                    except KeyError:
                        draft = None
                    else:
                        draft = True if dft.lower() in ['t', 'y', 'true', 'yes'] else False
                    try:
                        after = self.directives[sub]['after']
                    except KeyError:
                        after = None
                    else:
                        if after not in scenes.keys():
                            raise RuntimeError("In after={}, {} does not correspond to any other scene "
                                               "in the input".format(after, after))
                    scenelist.append(Scene(self, sub, tcl, res, pos, struct_list, traj_list, after, contour, ao,
                                           draft, max_trans_surf))
                    for action in scenes[sub]:
                        scenelist[-1].add_action(action)
        return scenelist

    def prepare(self):
        """
        Once text input is parsed, this fn sets
        global parameters such as fps, draft mode
        or whether to keep frames
        :return: None
        """
        try:
            self.fps = float(self.directives['global']['fps'])
        except KeyError:
            pass
        try:
            self.do_render = False if self.directives['global']['render'].lower() in ['n', 'f', 'no', 'false'] else True
        except KeyError:
            pass
        try:
            self.draft = True if self.directives['global']['draft'].lower() in ['y', 't', 'yes', 'true'] else False
        except KeyError:
            if not self.do_render:
                self.draft = True
        if not self.draft and os.name == 'nt':
            import pathlib
            print("Looking for Tachyon...")
            for pfiles in [x for x in os.listdir('C:\\') if x.startswith('Program') or x.startswith('User')]:
                candidates = sorted([str(x) for x in pathlib.Path('C:\\' + pfiles).glob('**/tachyon*.exe')])
                if candidates:
                    self.tachyon = candidates[0]
                    print('...found!')
                    break
            if not self.tachyon:
                raise RuntimeError("Tachyon was not found in system or user directories")
        for scene in self.scenes:
            if scene.draft is None:
                scene.draft = self.draft
        try:
            self.keepframes = True if self.directives['global']['keepframes'].lower() in ['y', 't', 'yes', 'true'] \
                else False
        except KeyError:
            pass
        try:
            self.breakpoints = [float(x) for x in self.directives['global']['breakpoints'].split(',')]
        except KeyError:
            pass
        try:
            self.gif = self.directives['global']['gif']
        except KeyError:
            pass
        try:
            self.name = self.directives['global']['name']
        except KeyError:
            pass
        try:
            self.restart = True if self.directives['global']['restart'].lower() in ['y', 't', 'yes', 'true'] else False
        except KeyError:
            pass
        master_ovls_parsed, master_ovls_counter = False, 0
        while not master_ovls_parsed:
            try:
                ovls_line = self.directives['master_overlay{}'.format(master_ovls_counter)]
            except KeyError:
                master_ovls_parsed = True
            else:
                # TODO check for 't=' somewhere
                ovl_action = SimultaneousAction(Scene(self, 'master_overlay_scene_{}'.format(master_ovls_counter)),
                                                ovls_line.replace('master_overlay', 'add_overlay'))
                ovl_action.initframe = int(float(ovl_action.parameters['start_time']) * self.fps)
                ovl_action.framenum = int(float(ovl_action.parameters['t'].strip('s')) * self.fps)
                self.master_overlays.append(ovl_action)
                master_ovls_counter += 1
        for scene in self.scenes:
            scene.calc_framenum()
        for scene in self.scenes:
            scene.merge_after()
    
    def check_path(self, filename):
        """
        Looks for the specified file in the local
        directory and at the location of the input
        file; raises a RuntimeError if file cannot
        be found
        :param filename: str, path (relative or absolute) of the file to be sought
        :return: None
        """
        if os.path.isfile(filename):
            return filename
        elif not os.path.isfile(filename) and '/' in self.scriptfile:
            prefix = '/'.join(self.scriptfile.split('/')[:-1]) + '/'
            if os.path.isfile(prefix + filename):
                return prefix + filename
            else:
                raise RuntimeError('File {} could not been found neither in the local directory '
                                   'nor in {}'.format(filename, prefix))
        else:
            raise RuntimeError('File {} not found, please make sure there are no typos in the name'.format(filename))
    
    @staticmethod
    def check_tcl(tcl_file):
        """
        If the files to be read by VMD were saved as
        absolute paths and then transferred to another
        machine, this fn will identify missing paths
        and look for the files in the working dir,
        creating another file if needed
        :param tcl_file: str, path to the VMD visualization state
        :return: str, new (or same) path to the VMD visualization state
        """
        inp = [line for line in open(tcl_file)]
        modded = False
        for n in range(len(inp)):
            if inp[n].strip().startswith('mol') and inp[n].split()[1] in ['new', 'addfile'] \
                    and inp[n].split()[2].startswith('/'):
                if not os.path.isfile(inp[n].split()[2]):
                    if os.path.isfile(inp[n].split()[2].split('/')[-1]):
                        print('Warning: absolute path {} was substituted with a relative path to the local file {}; '
                              'the modified .vmd file will be '
                              'backed up'.format(inp[n].split()[2], inp[n].split()[2].split('/')[-1]))
                        inp[n] = ' '.join(inp[n].split()[:2]) + " {} ".format(inp[n].split()[2].split('/')[-1]) \
                                 + ' '.join(inp[n].split()[3:])
                        modded = True
        if modded:
            with open(tcl_file + '.localcopy', 'w') as new_tcl:
                for line in inp:
                    new_tcl.write(line)
            return tcl_file + '.localcopy'
        else:
            return tcl_file
    
    def parse_audio(self, total_time):
        """
        Takes care of audio processing in several steps:
        first goes through a list of audio pieces to look
        for gaps and overlaps, trimming and creating silence;
        then parses each input audio file to match length etc.;
        finally combines all inputs (including patches of silence)
        into a single audio file and adds it to the previously
        rendered video file.
        :param total_time: float, total time of the movie (in seconds)
        :return: None
        """
        if len(self.audio) > 1:
            itrn = 0
            for au1, au2 in zip(self.audio[:-1], self.audio[1:]):
                if au1.movie_inittime + au1.length > au2.movie_inittime:
                    print("Audio from file {} would overlap with audio from file {}, "
                          "will be trimmed".format(au1.audiofile, au2.audiofile))
                    self.audio[itrn] = self.audio[itrn]._replace(length=au2.movie_inittime - au1.movie_inittime)
                itrn += 1
        # convert to a new list to add silence intervals between audio inputs
        new_audio_list = []
        from collections import namedtuple
        if self.audio[0].movie_inittime > 0:
            spacer = namedtuple("audio", "audiofile, movie_inittime, file_inittime, length, volume, fadein, fadeout")
            new_audio_list.append(spacer("", 0, 0, self.audio[0].movie_inittime, self.audio[0].volume,
                                         self.audio[0].fadein, self.audio[0].fadeout))
        for au1, au2 in zip(self.audio[:-1], self.audio[1:]):
            new_audio_list.append(au1)
            if au1.movie_inittime + au1.length < au2.movie_inittime:
                spacer = namedtuple("audio", "audiofile, movie_inittime, file_inittime, length, volume, fadein,fadeout")
                new_audio_list.append(spacer("", au1.movie_inittime + au1.length, 0,
                                             au2.movie_inittime - (au1.movie_inittime + au1.length), au1.volume,
                                             au1.fadein, au1.fadeout))
        if self.audio[-1].movie_inittime + self.audio[-1].length > total_time:
            self.audio[-1] = self.audio[-1]._replace(length=total_time - self.audio[-1].movie_inittime)
            new_audio_list.append(self.audio[-1])
        elif self.audio[-1].movie_inittime + self.audio[-1].length == total_time:
            new_audio_list.append(self.audio[-1])
        else:
            new_audio_list.append(self.audio[-1])
            spacer = namedtuple("audio", "audiofile, movie_inittime, file_inittime, length, volume, fadein, fadeout")
            new_audio_list.append(spacer("", self.audio[-1].movie_inittime + self.audio[-1].length, 0,
                                         total_time - (self.audio[-1].movie_inittime + self.audio[-1].length),
                                         self.audio[-1].volume, self.audio[-1].fadein, self.audio[-1].fadeout))
        # process the files to make sure they are trimmed properly
        for n, audio in enumerate(self.audio):
            din, dout = audio.fadein, audio.fadeout
            call_moly('{ff} -y -i {af} -q:a 0 -ss {start} -to {end} -af "afade=in:st={start}:d={din},'
                      'afade=out:st={end_out}:d={dout}" trimmed_audio{num}.mp3 >> {name}_ffmpeglog.moly '
                      '2>&1'.format(af=audio.audiofile, start=audio.file_inittime, din=din, dout=dout,
                               end=audio.file_inittime + audio.length, num=n, name=self.name,
                               end_out=audio.file_inittime + audio.length - dout, ff=self.ffmpeg), log=self.log)
            if audio.volume != 1.0:
                call_moly('{ff} -y -i trimmed_audio{n}.mp3 -q:a 0  -filter:a "volume={vol}" tmp.mp3 >> '
                          '{name}_ffmpeglog.moly 2>&1'.format(n=n, vol=audio.volume, name=self.name, ff=self.ffmpeg),
                          log=self.log)
                os.rename('tmp.mp3', 'trimmed_audio{n}.mp3'.format(n=n))
        # now the final concatenation with silence intermediates
        inputs = ' '.join(['-i trimmed_audio{}.mp3'.format(n, x.audiofile.split('.')[-1])
                           for n, x in enumerate(self.audio)])
        silence = ';\n'.join(['aevalsrc=0:d={}[s{}]'.format(x.length, n) for n, x in enumerate(new_audio_list)
                              if not x.audiofile])
        if silence:
            silence = '\n ' + silence + ';\n '
        concat_string = ''
        input_current = 0
        for n, audio in enumerate(new_audio_list):
            if audio.audiofile:
                concat_string = concat_string + '[{}:a]'.format(input_current)
                input_current += 1
            else:
                concat_string = concat_string + '[s{}]'.format(n)
        call_moly('{ff} -y {} -filter_complex "{}{}concat=n={}:v=0:a=1[aout]" -map [aout] {n}_audio.mp3 >> '
                  '{n}_ffmpeglog.moly 2>&1'.format(inputs, silence, concat_string, len(new_audio_list), n=self.name,
                                                   ff=self.ffmpeg), log=self.log)
        _ = [os.remove(f) for f in glob("trimmed_audio*")]

    def convert_to_gif(self):
        """
        When conversion to gif is requested, takes the final
        .mp4 files and converts them all to gifs; if parameters
        are wrongly specified, shows the ffmpeg command to save
        the user some time
        :return: None
        """
        if self.gif.lower() in ['y', 't', 'yes', 'true']:
            fps = 8
            width = 400
        else:
            if ',' in self.gif:
                fps, width = self.gif.split(',')
            else:
                raise RuntimeError("Wrong specification of parameters for gif conversion. To avoid re-running, consider"
                                   " calling 'ffmpeg -i [input].mp4 -r [fps] -vf scale=[width]:-1 [output].gif' "
                                   "directly from your command line, substituting parameters in [brackets] with "
                                   "desired values")
        for i in ["{}.mp4".format(self.name)] + glob("{}-part*.mp4".format(self.name)):
            call_moly('{} -i {} -y -r {} -vf scale={}:-1 {} >> {}_ffmpeglog.moly '
                      '2>&1'.format(self.ffmpeg, i, fps, width, i.replace('mp4', 'gif'), self.name), log=self.log)


class Scene:
    """
    A Scene instance is restricted to a single
    molecular system; all Scene parameters are
    read as input is parsed.
    """
    def __init__(self, script, name, tcl=None, resolution=(1000, 1000), position=(0, 0),
                 structure_list=None, trajectory_list=None, after=None, contour=None, ao=False, draft=False,
                 max_transp=1):
        self.script = script
        self.name = name
        self.alias = self.name  # one is permanent, one can be variable
        self.visualization = tcl
        self.actions = []
        self.resolution = resolution
        self.position = position
        self.structure_list = structure_list
        self.trajectory_list = trajectory_list
        self.contour = contour
        self.draft = draft
        self.ao = ao
        self.functions = []
        self.run_vmd = False
        self.total_frames = 0
        self.tachyon = None
        self.after = after
        self.first_frame = 0
        self.is_overlay = 0
        self.is_after = True if self.after is not None else False
        self.transparent_surfaces = max_transp
        self.counters = {'hl': 0, 'overlay': 0, 'make_transparent': 0, 'make_opaque': 0, 'rot': 0, 'zoom': 0,
                         'translate': 0}
        self.labels = {'Atoms': [], 'Bonds': []}
    
    def add_action(self, description):
        """
        Adds an action to the subscript
        :param description: str, description of the action
        :return: None
        """
        if not description.strip().startswith('{'):
            self.actions.append(Action(self, description))
        else:
            self.actions.append(SimultaneousAction(self, description.strip('{} ')))

    def show_script(self):
        """
        Shows actions scheduled for rendering
        within the current subscript; mostly
        for debugging purposes
        :return: None
        """
        for action in self.actions:
            print(action)
    
    def calc_framenum(self):
        """
        Once the fps rate is known, we can go through all actions
        and set integer frame counts as needed. Note: some actions
        can be instantaneous (e.g. recenter camera), so that
        not all will have a non-zero framenum. Also, the cumulative
        frame number (for the entire Scene) will be calculated.
        :return: None
        """
        fps = self.script.fps
        cumsum = self.first_frame
        for action in self.actions:
            action.initframe = cumsum
            try:
                action.framenum = int(float(action.parameters['t'])*fps)
            except KeyError:
                action.framenum = 0
            cumsum += action.framenum
        self.total_frames = cumsum
    
    def merge_after(self):
        """
        Re-processes frame numberings, scene
        names etc. if the current Scene is meant
        to follow another Scene (specified by setting
        'after=previous_scene' in the Scene input)
        :return: None
        """
        if self.after:
            ref_scene = [sc for sc in self.script.scenes if sc.alias == self.after][0]
            self.first_frame = ref_scene.total_frames
            self.calc_framenum()
            self.name = ref_scene.name
            
    def tcl(self):
        """
        This is the top-level function that produces
        an executable TCL script based on the corresponding
        action.generate() functions; also, many defaults are
        set here to override VMD's internal settings
        :return: str, the TCL code to be executed
        """
        if self.visualization or self.structure_list or any([str(act) in Action.actions_requiring_tcl
                                                             for act in self.actions]):
            self.run_vmd = True
            if self.visualization:
                code = [line for line in open(self.visualization, 'r').readlines() if not line.startswith('#')]
                code = ''.join(code)
            elif self.structure_list:
                code = ''
                for nstr, structure in enumerate(self.structure_list):
                    code += 'mol new {} type {} first 0 last -1 step 1 filebonds 1 ' \
                            'autobonds 1 waitfor all\n'.format(structure, structure.split('.')[-1])
                    if len(self.trajectory_list) >= nstr+1:
                        traj = self.trajectory_list[nstr]
                        code += 'mol addfile {} type {} first 0 last -1 step 1 filebonds 1 ' \
                                'autobonds 1 waitfor all\n'.format(traj, traj.split('.')[-1])
                    code += 'mol delrep 0 top\nmol representation NewCartoon 0.300000 10.000000 4.100000 0\n' \
                            'mol color Structure\nmol selection {all}\nmol material Opaque\nmol addrep top\n' \
                            'color Display Background white\ndisplay projection Orthographic\n'
            else:
                code = 'color Display Background white\ndisplay projection Orthographic\n'
            code += 'foreach molnumber [molinfo list] {set repnums$molnumber [list]}\n'  # each mol has its replist
            code += 'axes location off\ncolor add item Type C yellow\ncolor Type C yellow\n' \
                    'color add item Element C black\ncolor Element C black\ndisplay depthcue off\n'
            if self.ao:
                code += 'display ambientocclusion on\ndisplay aoambient 0.82\ndisplay aodirect 0.25\n'
                if self.draft:
                    warnings.warn("Warning: Ambient Occlusion will not affect the outcome in the draft mode")
            if not self.draft:
                if os.name == 'posix':
                    tach = '$env(TACHYON_BIN)'
                else:
                    tach = self.script.tachyon.replace('\\', '\\\\')
                code += 'render options Tachyon \"{}\" -aasamples 12 %s -format TARGA -o %s.tga ' \
                        '-trans_max_surfaces {} -res {} {}\n'.format(tach, self.transparent_surfaces, *self.resolution)
            else:
                if os.name == 'posix':
                    try:
                        screen_res = str(os.popen("xdpyinfo | grep dimensions | awk '{print $2}'").read().strip()).\
                            split('x')
                        screen_res = [int(x) for x in screen_res]
                    except:
                        warnings.warn("Cannot determine actual screen size; make sure your resolution does not exceed "
                                      "screen resolution in the draft mode -- frames might be trimmed otherwise.")
                    else:
                        if screen_res[0] < self.resolution[0] or screen_res[1] < self.resolution[1]:
                            raise RuntimeError("In the draft mode, scene resolution ({}x{}) should be smaller than your"
                                               " screen resolution ({}x{}), otherwise the resulting frames might not "
                                               "be sized and shaped properly.".format(*self.resolution, *screen_res))
                else:
                    if self.resolution[0] > 1024 or self.resolution[1] > 800:
                        print("Windows users: Note that in the draft mode, the size of a single Scene will be limited "
                              "by your screen resolution - be careful when using high resolutions!")
                code += 'display resize {res}\nafter 100\ndisplay update\nafter 100\ndisplay resize {res}\n' \
                        'display rendermode GLSL\n'.format(res=' '.join(str(x) for x in self.resolution))
            action_code = ''
            for ac in self.actions:
                action_code += ac.generate_tcl()
            if action_code:
                code += action_code
        else:
            code = ''
        if all([ac.already_rendered for ac in self.actions]):
            self.run_vmd = False
            print("Skipping scene {}, all frames have already been rendered".format(self.name))
        return code + '\nexit\n'
        
        
class Action:
    """
    Intended to represent a single action in
    a movie, e.g. a rotation, change of material
    or zoom-in
    """
    
    allowed_params = {'do_nothing': {'t'},
                      'show_grid': set(),
                      'animate': {'frames', 'smooth', 't', 'molecules'},
                      'rotate': {'angle', 'axis', 't', 'sigmoid', 'fraction', 'abruptness', 'molecules'},
                      'translate': {'vector', 't', 'sigmoid', 'fraction', 'abruptness', 'molecules'},
                      'zoom_in': {'scale', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'zoom_out': {'scale', 't', 'sigmoid', 'fraction', 'abruptness'},
                      'make_transparent': {'material', 't', 'sigmoid', 'limit', 'start', 'fraction', 'abruptness'},
                      'highlight': {'selection', 't', 'color', 'mode', 'style', 'alias', 'thickness', 'material',
                                    'abruptness', 'alpha', 'isovalue', 'fade_in', 'fade_out', 'smooth', 'cutoff',
                                    'multiframe', 'molecules'},
                      'make_opaque': {'material', 't', 'sigmoid', 'limit', 'start', 'fraction', 'abruptness'},
                      'center_view': {'selection', 'molecules'},
                      'insert_tcl': {'file', 'code', 'range', 'loopover', 'loop_command', 't'},
                      'show_figure': {'figure', 't', 'datafile', 'dataframes', 'dataframes_from_file'},
                      'add_overlay': {'figure', 't', 'origin', 'relative_size', 'dataframes', 'dataframes_from_file',
                                      'aspect_ratio', 'datafile', '2D', 'text', 'textsize', 'sigmoid', 'alpha', 'scene',
                                      'transparent_background', 'textcolor', 'decimal_points', 'textbox', 'angle',
                                      'movie', 'from', 'length', 'seaborn', 'mode', 'alias', 'start_time', 'center'},
                      'add_label': {'label_color', 'atom_index', 'label', 'text_size', 'alias', 'offset'},
                      'remove_label': {'alias', 'all'},
                      'add_audio': {'audiofile', 'from', 'length', 'volume', 'fade_in', 'fade_out'},
                      'add_distance': {'selection1', 'selection2', 'label_color', 'text_size', 'alias', 'bead'},
                      'remove_distance': {'alias', 'all'},
                      'fit_trajectory': {'selection', 't', 'axis', 'invert', 'abruptness', 'molecules', 'frame',
                                         'selection_ref', 'molecule_ref', 'frame_ref'},
                      'toggle_molecule': {'molecule_id', 'top', 'freeze', 'active', 'drawn'}
                      }

    allowed_actions = list(allowed_params.keys())

    actions_requiring_tcl = ['do_nothing', 'animate', 'rotate', 'zoom_in', 'zoom_out', 'make_transparent',
                             'make_opaque', 'center_view', 'add_label', 'remove_label', 'highlight', 'insert_tcl',
                             'fit_trajectory', 'add_distance', 'remove_distance', 'translate', 'toggle_molecule']
    
    def __init__(self, scene, description):
        self.scene = scene
        self.description = description
        self.action_type = None
        self.parameters = OrderedDict()  # will be a dict of action parameters
        self.initframe = None  # contains the initial frame number in the overall movie's numbering
        self.framenum = None  # total frames count for this action
        self.highlights, self.transp_changes = OrderedDict(), OrderedDict()
        self.rots, self.transl, self.zoom = OrderedDict(), OrderedDict(), OrderedDict()
        self.already_rendered = False
        self.parse(description)
    
    def __repr__(self):
        return self.description.split()[0]
    
    def generate_tcl(self):
        """
        Should yield the TCL code that will
        produce the action in question; in case
        of restarting, checks whether frames have
        been rendered already for this action
        :return: str, TCL code
        """
        
        if set(self.action_type).intersection(set(Action.actions_requiring_tcl)):
            if self.scene.script.restart:
                self.check_if_rendered()
            return tcl_actions.gen_loop(self)
        else:
            self.already_rendered = True
            return ''
        
    def check_if_rendered(self):
        """
        In case of restarting, checks whether frames have
        been rendered already for this action
        :return: None
        """
        if all(['{}-{}.png'.format(self.scene.name, f) in os.listdir('.') or
                '{}-{}.tga'.format(self.scene.name, f) in os.listdir('.') for f in
                range(self.initframe, self.initframe + self.framenum)]):
            if any(['{}-{}.tga'.format(self.scene.name, f) in os.listdir('.') for f in
                    range(self.initframe, self.initframe + self.framenum)]):
                for f in glob('{}-*tga'.format(self.scene.script.name)):
                    call_moly('{} {} {}'.format(self.scene.script.convert, f, f.replace('tga', 'png')),
                              log=self.scene.script.log)
                    os.remove(f)
            self.already_rendered = True
        elif all(['{}-{}.png'.format(self.scene.script.name, f) in os.listdir('.') for f in
                  range(self.initframe, self.initframe + self.framenum)]):
            for f in glob('{}-*png'.format(self.scene.script.name)):
                os.rename(f, f.replace(self.scene.script.name, self.scene.name))
            self.already_rendered = True
    
    def generate_graph(self):
        """
        Runs external functions that take care of
        on-the-fly rendering of matplotlib graphs
        or copying of external images
        :return: None
        """
        actions_requiring_genfig = ['show_figure', 'add_overlay']
        if set(self.action_type).intersection(set(actions_requiring_genfig)):
            graphics_actions.gen_fig(self)
        elif 'show_grid' in self.action_type:
            graphics_actions.show_grid(self)

    def parse(self, command, ignore=()):
        """
        Parses a single command from the text input
        and converts into action parameters
        :param command: str, description of the action
        :param ignore: tuple, list of parameters to ignore while parsing
        (these will be stored in special-purpose dicts to avoid interference)
        :return: None
        """
        spl = self.split_input_line(command)
        if spl[0] not in Action.allowed_actions:
            raise RuntimeError("'{}' is not a valid action. Allowed actions "
                               "are: {}".format(spl[0], ', '.join(list(Action.allowed_actions))))
        if not isinstance(self, SimultaneousAction) and spl[0] == "add_overlay":
            if "mode=d" not in spl:
                raise RuntimeError("Overlays can only be added simultaneously with another action, not as"
                                   "a standalone one")
        self.action_type = [spl[0]]
        new_dict = self.line_to_parmdict(spl, ignores=ignore)
        for par in new_dict:
            if par not in Action.allowed_params[spl[0]]:
                raise RuntimeError("'{}' is not a valid parameter for action '{}'. Parameters compatible with this "
                                   "action include: {}".format(par, spl[0],
                                                               ', '.join(list(Action.allowed_params[spl[0]]))))
        self.parameters.update(new_dict)
        if 't' in self.parameters.keys():
            self.parameters['t'] = self.parameters['t'].rstrip('s')
        if not isinstance(self, SimultaneousAction):
            if spl[0] == 'highlight':
                try:
                    alias = '_' + self.parameters['alias']
                except KeyError:
                    alias = self.scene.counters['hl']
                self.highlights = OrderedDict({'hl{}'.format(alias): self.parameters})
                self.scene.counters['hl'] += 1
            if spl[0] in ['make_transparent', 'make_opaque']:
                self.transp_changes = {spl[0]: self.parameters}
                self.scene.counters[spl[0]] += 1
            if spl[0] == 'rotate':
                self.rots = OrderedDict({'rot0': self.parameters})
            if spl[0] == 'translate':
                self.transl = OrderedDict({'translate0': self.parameters})
            if spl[0].startswith('zoom_'):
                self.zoom = OrderedDict({'zoom': self.parameters})

    @staticmethod
    def split_input_line(line):
        """
        A modified string splitter that doesn't split
        words encircled in quotation marks; required
        by actions that accept a VMD-compatible
        selection string
        :param line: str, line to be split
        :return: list of strings, contains individual words
        """
        line = line.strip()
        words = []
        open_quotation = False
        quot_mark = '"'
        previous = 0
        for current, char in enumerate(line):
            if char in ["'", '"']:
                if not open_quotation:
                    open_quotation = True
                    quot_mark = char
                elif open_quotation and char == quot_mark:
                    open_quotation = False
            if (char == ' ' and not open_quotation) or current == len(line) - 1:
                word = line[previous:current+1].strip()
                if word:
                    words.append(word)
                previous = current
        return words

    @staticmethod
    def within_quotes(line, position):
        line = line.strip()
        open_quotation = False
        quot_mark = '"'
        for current, char in enumerate(line):
            if char in ["'", '"']:
                if not open_quotation:
                    open_quotation = True
                    quot_mark = char
                elif open_quotation and char == quot_mark:
                    open_quotation = False
            if current == position:
                return open_quotation
        return False

    @staticmethod
    def line_to_parmdict(spl, ignores=tuple()):
        new_dict = OrderedDict()
        for prm in spl[1:]:
            try:
                if prm.split('=')[0] not in ignores:
                    quote = '"' if prm.split('=')[1].startswith('"') and prm.split('=')[-1].strip().endswith('"') \
                        else "'"
                    new_dict.update({prm.split('=')[0]: '='.join(prm.split('=')[1:]).strip(quote)})
            except IndexError:
                command = ' '.join(spl)
                raise RuntimeError("Line '{}' is not formatted properly; action name should be followed by keyword="
                                   "value pairs, and no spaces should encircle the '=' sign".format(command))
        return new_dict
        

class SimultaneousAction(Action):
    """
    Intended to represent a number of actions
    that take place simultaneously (e.g. zoom
    and rotation)
    """
    def __init__(self, scene, description):
        self.overlays = OrderedDict()  # need special treatment for overlays as there can be many ('ov0', 'ov1', ...)
        self.highlights = OrderedDict()  # the same goes for highlights ('hl0', 'hl1', ...)
        self.transp_changes = OrderedDict()  # ...and for make_opaque/make_transparent
        super().__init__(scene, description)
        
    def parse(self, command, ignore=()):
        """
        We simply add action parameters to the
        params dict, assuming there will be no
        conflict of names (need to ensure this
        when setting action syntax); this *is*
        a workaround, but should work fine for
        now - might write a preprocessor later
        to pick up and fix any possible issues
        :param command: str, description of the actions
        :param ignore: tuple, list of parameters to ignore while parsing
        :return: None
        """
        actions = [comm.strip() for comm in command.split(';') if comm]
        for action in actions:
            igns = []  # ones that we don't want to be overwritten in the 'parameters' dict
            if action.split()[0] == 'add_overlay':
                self.parse_many(action, self.overlays, 'overlay')
                igns.append('figure')
                igns.append('mode')
                igns.append('alias')
                igns.append('from')
                igns.append('length')
                igns.append('angle')
            elif action.split()[0] == 'highlight':
                self.parse_many(action, self.highlights, 'hl')
                igns.append('selection')
                igns.append('mode')
                igns.append('alias')
                igns.append('molecules')  # TODO check if won't interfere w/fitting
            elif action.split()[0] in ['make_transparent', 'make_opaque']:
                self.parse_many(action, self.transp_changes, action.split()[0])
                igns.append('fraction')
            elif action.split()[0] == 'rotate':
                self.parse_many(action, self.rots, 'rot')
                igns.append('axis')
                igns.append('fraction')
                igns.append('molecules')
            elif action.split()[0].startswith('zoom_'):
                self.parse_many(action, self.zoom, 'zoom')
                igns.append('fraction')
            elif action.split()[0] == 'translate':
                self.parse_many(action, self.transl, 'translate')
                igns.append('molecules')
            elif action.split()[0] in ['center_view', 'add_label', 'remove_label',
                                       'add_distance', 'remove_distance', 'toggle_molecule']:
                raise RuntimeError("{} is an instantaneous action (i.e. doesn't last over finite time interval) and "
                                   "cannot be combined with finite-time ones".format(action.split()[0]))
            super().parse(action, tuple(igns))
        self.action_type = [action.split()[0] for action in actions]
        if 'zoom_in' in self.action_type and 'zoom_out' in self.action_type:
            raise RuntimeError("Actions {} are mutually exclusive".format(", ".join(self.action_type)))
        # if 'add_overlay' in self.action_type and 'scene' in self.parameters:  TODO this should be done after parsing
        #     if self.parameters['scene'] not in self.scene.script.scenes:
        #         raise RuntimeError("Scene {} requested as overlay, but not defined properly "
        #                            "in the input".format(self.parameters['scene']))
        if 't' not in self.parameters:
            raise RuntimeError("You can only combine finite-time actions using curly brackets. In directive "
                               "\n\n\t{}\n\n the duration is not specified; either rewrite it as consecutive "
                               "instantaneous actions, or add the 't=...s' parameter to one of them".format(command))
    
    def parse_many(self, directive, actions_dict, keyword):
        """
        Several types of actions have non-unique
        keywords or can be defined multiple times
        per Action, and hence are specifically handled
        by this function to put the params into
        a separate dictionary (e.g. self.highlights)
        :param directive: str, input section that defines a single Action in SimultaneousAction
        :param actions_dict: dict, the dictionary to handle the given action
        :param keyword: str, unique name of the action (e.g. 'highlight1')
        :return: None
        """
        actions_count = self.scene.counters[keyword]
        self.scene.counters[keyword] += 1
        spl = self.split_input_line(directive)
        prm_dict = Action.line_to_parmdict(spl)
        if 'alias' in prm_dict.keys():
            alias = '_' + prm_dict['alias']
        elif keyword == 'zoom':
            alias = ''
        else:
            alias = str(actions_count)
        actions_dict[keyword + alias] = prm_dict
    

def molywood():
    """
    This is the initial entry point for the script,
    accessible both from the command line
    and when the script is run manually
    :return: None
    """
    if not (sys.version_info[0] == 3 and sys.version_info[1] >= 4):
        raise RuntimeError("You need at least Python 3.4 to run Molywood, please upgrade and reinstall")
    try:
        input_name = sys.argv[1]
    except IndexError:
        gen_example()
    else:
        if input_name in ['-h', '--help']:
            print_help()
            sys.exit(0)
        run_script(input_name)


def print_logo():
    print("\n\n   :o++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++o.   \n"
          "  +s`               `.-:://////:::-`            `/sysoo+/:-.`                  `.--:::::--..`  `h.  \n"
          "  dsss+-`         .oddhhyyssssssssss/.         -hdmmdyssssssso+:.           `/hddhhyssssssssso/-o/  \n"
          "  mssssssyy++hdy+smNNdhhhysssssssssssssdds+ohdyhdNNmhyssssssssssssho+sddo+odmdhhmmdhysssssssssssh+  \n"
          "  mssssssys::dMh+odMmsshNdyssssssssssssmM+::NMhssNMdsyssssssssssssh::oMM/:+MMyssMMysyyssssssssssd+  \n"
          "  msssssssy::::oooooooossssysssssssssssy+::::ooosNMmssyssssssssssss+:sMM++osssossssossysssssssssd+  \n"
          "  mssssssss/  `::::::::///+yysssssssssss+   `::::mMh//yyssssssssssso.-MM-:::::////////yyssssssssd+  \n"
          "  myysssssss: ::::::::::::/ohyyyyyyyyyyys-  :::::mMh::ohyssssssssssso/MM/:::::::::////oyysssssssd+  \n"
          "  myyyyyyyyyy+:::::::::::::-yhhhhhhyyyyyys`-:::::mMh::/yhyyyyyyyyyyyyyNM/:::::::::::/-.yyyyyyyyyd+  \n"
          "  mhhhhhhhhhhyo:::::::::::: /hhhhhhhhhhhhy+::::::mMh:::/yhhhhhhhhhhhhhhN/:::::::::::.  +hhhhyyyyd+  \n"
          "  mhhhhhhhhhhhho::::::::::. :dhhhhhhhhhhhhy/:::::mMy::::-yhhhhhhhhhhhhhd/::::::::::.   .hhhhhhhhd+  \n"
          "  mhhhhddddmmmddo/////////..+Ndhhhhhhhdddddh+////mMh///-.:dhhhhhdddddddds//////////.....+hhhhhhhm+  \n"
          "  mdddmmmmmmmmmmdhdNmsshNm++yMmddddddmmmmmmmddhssNMms+hmh++dmmmmmmmmmmmmdysNNyssNNs/+dmy+sddddddN+  \n"
          "  m+dmmmmmmmmmmmmddNdooyNm/:oNmddmmmmmmmmmmmmmdyodNh//hNh/:ydmmmmmmmmmmmmdsNNsooNNo:/dNs:/hdmmmmN+  \n"
          "  m +dmmmmmmmmmmmmddhs+-......../hdmmmmmmmddddhhyo:........./dmmmmmmmmmmmmdhhyyy+..........-ohdmN+  \n"
          "  m  +dmmmmmmmddhyo:.`           `-://///::--.``             -ydmmmmmmmmmmddhs+-             `-:y+  \n"
          "  m   -+ooo+/:-.`                                             `-/+oooo++/:-.`                   ++  \n"
          "  m   `++/   /++     ````              -/:  -/:   -++` -+  :++`    ````       ````    -+++++-   ++  \n"
          "  m   .MMM/ oMMN   .ymmmd+`  -hh:      :NM+-NMo   /MM/ dM: mMm   `odmmms.   :hmmmd/   sMMmmMNo  ++  \n"
          "  m   .MMMNoMMMN   dMN+sMMo  :MM/       +MNmMy    `NMd`MMs:MMs   oMMo+NMh  `MMd+yMM-  sMM.`NMd  ++  \n"
          "  m   .MMMMMMMMN   dMm -MMo  :MM/        yMMd`     yMMyMMmhMM.   sMM. NMd  `MMy +MM:  sMM. NMd  ++  \n"
          "  m   .MMNMMMMMN   dMm -MMo  :MM/        -MMo      :MMMMMMMMd    sMM. NMd  `MMy +MM:  sMM. NMd  ++  \n"
          "  m   .MMyhMsdMN   dMm`-MMo  :MM/        -MMo       NMMNsMMM+    sMM.`NMd  `MMy`+MM:  sMMo+NMh  ++  \n"
          "  d`  `NNo`s`yNm   sMMmmMN:  :MMdhhy     -NN+       oNNy.NNm`    /NMmmMMs   dMNmNMm.  oNNNNNy.  +/  \n"
          "  +o                -++++`   -yyyyys      ``                      .++++-     :+++/`            .h`  \n"
          "   :o++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++o`   \n\n")


def print_help():
    try:
        wd = int(Popen(['stty', 'size'], stdout=PIPE, stderr=PIPE).communicate()[0].decode().strip().split()[1])
    except:
        pass
    else:
        if wd > 100:
            print_logo()
    print('\n          This is the command-line tool that produces a movie based on a text input file.'
          '\n         To run it, simply provide the text input as an argument in the command line, e.g.\n'
          '\n                                   molywood input_file.txt\n'
          '\n         To generate a sample input file, type "molywood" and select "i" when prompted to;'
          '\n        you can then modify the file sample_molywood_input.txt according to your preference.\n'
          '\n        For documentation, examples and guidance, visit http://mmb.irbbarcelona.org/molywood\n'
          '\n         Source files for the examples can be found on http://gitlab.com/KomBioMol/molywood\n')


def run_script(input_name):
    """
    The main entry point for the script, allows
    for easy testing with an additional -test
    parameter in the command line
    :param input_name: path to the input file
    :return: None
    """
    if len(sys.argv) <= 2:
        scr = Script(input_name)
        scr.render()
    else:
        test_param = sys.argv[2]
        if test_param == '-test':
            scr = Script(input_name)
            for sscene in scr.scenes:
                stcl_script = sscene.tcl()
                if sscene.run_vmd:
                    with open('script_{}.tcl'.format(sscene.alias), 'w') as sout:
                        sout.write(stcl_script)
        elif test_param == '-log':
            print("Will log all command-line activity")
            with open('command_line_log.moly', 'w') as outfile:
                outfile.write('')
            scr = Script(input_name, log=True)
            scr.render()
        else:
            print("\n\nWarning: parameters beyond the first will be ignored\n\n")
            scr = Script(input_name)
            scr.render()


def gen_yml():
    """
    Generates the .yml file on-the-fly when extra
    dependencies need to be installed; this is convenient
    as we do not need to re-install existing dependencies
    in the new virtual environment, saving disk space.
    This fn also installs the venv.
    :return: None
    """
    if not (sys.version_info[0] == 3 and sys.version_info[1] >= 4):
        raise RuntimeError("You need at least Python 3.4 to run Molywood, please upgrade and reinstall")
    deps_to_install, channels_to_install = check_deps()
    if not deps_to_install:
        print("all requirements satisfied, no need to create a venv")
        return
    conda = 'conda' if os.name == 'posix' else 'conda.exe'
    conda_present = True if which(conda) else False
    if conda_present:  # with conda, we can install everything we want
        genenv_present = 'molywood' in os.popen("{} info --envs".format(conda)).read()
        if genenv_present:
            print("\n\n *** Please type 'source activate molywood'\n\n (or 'conda activate molywood', depending on "
                  "your conda setup) \n\n to activate the virtual environment. \n\n Alternatively, run "
                  "conda env remove --name molywood to remove the existing one, \n\n and re-run molywood-gen-env"
                  "to reinstall it from scratch. ***")
            return
        if 'environment.yml' in os.listdir('.'):
            os.rename('environment.yml', 'bak_environment.yml')
        print('\n Do you want to create a new conda environment called "molywood" \n '
              '(might take up more space), or only add dependencies to the current one \n '
              '(faster and lighter, but less modular)?\n\n')
        ans = input(" Type 'n' to create a new one, or 'u' to update existing one:\n >>> ")
        while ans not in ['u', 'n']:
            ans = input(" Type 'n'  or 'u':\n >>> ")
        if ans == 'u':
            env = [x.decode() for x in check_output(['conda', 'env', 'list']).splitlines() if '*' in x.decode()][0]
            curr_env = env.split()[0]
            with open('environment.yml', 'w') as envfile:
                envfile.write('name: {}\n'.format(curr_env))
                envfile.write('channels:\n')
                for chan in channels_to_install:
                    envfile.write('- {}\n'.format(chan))
                envfile.write('dependencies:\n')
                for dep in deps_to_install:
                    if dep == 'magick':
                        dep = 'imagemagick'
                    if os.name == 'posix':
                        envfile.write('- {}\n'.format(dep))
                    else:
                        if dep == 'vmd':
                            print('On Windows, VMD cannot be installed automatically via conda; please go to '
                                  'https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD '
                                  'and install manually in C:\\\\Program Files or C:\\\\Users')
                        elif dep == 'imagemagick':
                            print('On Windows, imagemagick cannot be installed automatically via conda; please go to '
                                  'https://imagemagick.org/script/download.php and install manually in C:\\\\Program '
                                  'Files or C:\\\\Users')
                        else:
                            envfile.write('- {}\n'.format(dep))
            call_moly('{} env update --file environment.yml'.format(conda))
        else:
            full_yml = 'name: molywood\nchannels:\n  - conda-forge\n  - menpo\ndependencies:\n  - python >3.4,<3.9\n' \
                       '  - vmd\n  - ffmpeg\n  - imagemagick\n  - conda\n  - numpy\n  - matplotlib\n  - seaborn\n'
            with open('environment.yml', 'w') as envfile:
                envfile.write(full_yml)
            call_moly('{} env create'.format(conda))
        os.remove('environment.yml')
        if 'bak_environment.yml' in os.listdir('.'):
            os.rename('bak_environment.yml', 'environment.yml')
    else:  # otherwise, we can only install python stuff and hope for the best
        deps_python = {'numpy', 'matplotlib', 'seaborn'}
        deps_python = deps_python.intersection(set(deps_to_install))
        if deps_python:
            import subprocess
            for dep in deps_python:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--user"])
            print("Python dependencies successfully installed")
        missing_deps, _ = check_deps()
        if missing_deps:
            print("\n\n *** Missing dependencies still present. \n\n Consider downloading Anaconda "
                  "and re-running this tool, \n\n or installing the following dependencies manually: \n\n")
            manual_install()


def check_deps(printing=True):
    """
    Tests for dependencies, both python libraries
    (numpy, matplotlib, seaborn) and other software
    (ffmpeg, vmd, imagemagick); returns a list of
    missing dependencies and corresponding conda
    channels to get them from
    :param printing: bool, whether to print the
    results of individual checks
    :return: list of str, missing dependencies
             list of str, channels from which to download them
    """
    if os.name == 'posix':
        vmd, ffmpeg, compose, conda = 'vmd', 'ffmpeg', 'composite', 'conda'
    elif os.name == 'nt':
        vmd, ffmpeg, compose, conda = 'vmd.exe', 'ffmpeg.exe', 'magick.exe', 'conda'
    else:
        raise RuntimeError("OS could not be detected")
    
    def check_external():
        deps = set()
        channels = set()
        if not which(vmd):
            deps.add('vmd')
            channels.add('conda-forge')
            if printing:
                print('vmd not found in PATH')
        if not which(ffmpeg):
            deps.add('ffmpeg')
            channels.add('menpo')
            if printing:
                print('ffmpeg not found in PATH')
        if not which(compose):
            deps.add('magick')
            channels.add('conda-forge')
            if printing:
                print('imagemagick not found in PATH')
        return deps, channels
    
    deps_to_install, channels_to_install = check_external()
    if os.name == 'nt' and deps_to_install:  # on Windows, we do an extra round of checking in Program Files etc.
        channels_to_install = {'conda-forge', 'menpo'}
        import pathlib
        print('will try harder looking for {}'.format(', '.join(list(deps_to_install))))
        extra_search = ['conda'] if not which(conda) else []
        for sought in list(deps_to_install) + extra_search:
            found = 0
            for pfiles in [x for x in os.listdir('C:\\') if x.startswith('Program') or x.startswith('User')]:
                candidates = sorted([str(x) for x in pathlib.Path('C:\\' + pfiles).glob('**/{}.exe'.format(sought))],
                                    key=lambda x: len(str(x)))
                if candidates:
                    os.environ['PATH'] = os.environ['PATH'] + ';' + os.sep.join(candidates[0].split(os.sep)[:-1])
                    found += 1
                    print('{} found in dir {}'.format(sought, os.sep.join(candidates[0].split(os.sep)[:-1])))
            if found > 0 and sought in deps_to_install:
                deps_to_install.remove(sought)
    try:
        import numpy
    except ImportError:
        deps_to_install.add('numpy')
        channels_to_install.add('conda-forge')
        if printing:
            print('numpy not found')
    try:
        import matplotlib
    except ImportError:
        deps_to_install.add('matplotlib')
        channels_to_install.add('conda-forge')
        if printing:
            print('matplotlib not found')
    try:
        import seaborn
    except ImportError:
        deps_to_install.add('seaborn')
        channels_to_install.add('conda-forge')
        if printing:
            print('seaborn not found')
    return deps_to_install, channels_to_install


def manual_install():
    """
    Prints suggestions on manual installation of dependencies
    if some are missing and cannot be installed automatically
    :return: None
    """
    missing_deps, _ = check_deps(printing=False)
    if os.name == 'posix':
        or_else = "or through 'sudo apt-get install {x}' (Debian/Ubuntu/Mint), 'brew install {x}' (OSX) " \
                  "or your package manager of choice"
    else:
        or_else = ''
    if 'vmd' in missing_deps:
        print("  * VMD from https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD\n\n")
    if 'ffmpeg' in missing_deps:
        print("  * ffmpeg from https://www.ffmpeg.org/download.html {}\n\n".format(or_else.format(x='ffmpeg')))
    if 'magick' in missing_deps:
        print("  * Imagemagick from https://imagemagick.org/script/download.php "
              "{}\n\n".format(or_else.format(x='imagemagick')))
    if 'numpy' in missing_deps:
        print("  * numpy through 'pip install numpy' or through your Python IDE")
    if 'matplotlib' in missing_deps:
        print("  * matplotlib through 'pip install matplotlib' or through your Python IDE")
    if 'seaborn' in missing_deps:
        print("  * seaborn through 'pip install seaborn' or through your Python IDE")


def gen_example():
    """
    Generates a sample input file to be shown as an example
    when 'molywood' is run with no input args
    :return: None
    """
    ex_input = '$ global fps=10 render={} draft={} name=sample_movie\n' \
               '$ scene pdb_code=1w0t resolution=750,750\n' \
               '\n' \
               '# scene\n' \
               'zoom_in            scale=1.4\n' \
               'fit_trajectory     axis=y selection="nucleic and not backbone"\n' \
               'make_transparent   material=Opaque\n' \
               'highlight          selection="nucleic and noh" material=Diffuse style=licorice color=type mode=u\n' \
               'highlight          selection=protein material=Diffuse style=quicksurf color=white mode=u\n' \
               '{{rotate  axis=y angle=720 t=2s sigmoid=sls fraction=:0.25; zoom_in scale=1.5}}\n' \
               'rotate  axis=y angle=720 t=2s sigmoid=sls fraction=0.25:0.5\n' \
               'rotate  axis=y angle=720 t=2s sigmoid=sls fraction=0.5:0.75\n' \
               '{{rotate  axis=y angle=720 t=2s sigmoid=sls fraction=0.75:; zoom_out scale=1.5}}\n'
    ans = input("\n Warning: no input data was provided. \n\n To run Molywood, provide the name of the input file, "
                "e.g. 'molywood script.txt'. \n\n To run a sample visualization, type 'y'. \n\n To generate a sample "
                "input, type 'i'. \n\n Pressing 'Enter' (or entering any other command) will terminate the script.\n "
                ">>> ")
    if ans == 'y':
        ans2 = input(" Do you want to render the movie ('r'), or display only ('d')?\n >>> ")
        while ans2.lower() not in 'rd':
            ans2 = input(" Type 'r' or 'd':\n >>> ")
        if os.name == 'posix':
            display = os.popen("xdpyinfo | grep dimensions 2>&1").read()
        else:
            display = True
        render = 't' if ans2 == 'r' else 'f'
        if not display and not render:
            print(" Sorry - no display detected, I can only render for you here!")
            sys.exit(1)
        print(' Sample movie with pdb 1w0t, render mode {}'.format('on' if ans2 == 'r' else 'off'))
        draft = 't' if display else 'f'
        if draft == 'f':
            print("No display was detected, cannot use the draft mode; switching to Tachyon for rendering")
        with open('sample_molywood_input.txt', 'w') as sample_inp:
            sample_inp.write(ex_input.format(render, draft))
        run_script('sample_molywood_input.txt')
    elif ans == 'i':
        with open('sample_molywood_input.txt', 'w') as sample_inp:
            sample_inp.write(ex_input.format('f', 't'))
    else:
        print(' Ok, terminating')
        sys.exit(0)
        

def call_moly(arg, answer=False, log=False):
    """
    A wrapper to consistently take care of all external calls
    :param arg: str, a command to be run from the command line
    :param answer: bool, whether to return the captured output
    :param log: bool, whether to log the command to a file
    :return: str, captured output from the command
    """
    result = call(arg, shell=True)
    if log:
        with open('command_line_log.moly', 'a') as outfile:
            outfile.write(arg + '\n')
    if answer:
        return result


if __name__ == "__main__":
    molywood()
