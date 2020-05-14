# Project structure

* Description of the experiment and sample: CIF files
    * Phases directory with individual cif files for every phase (those files are named the same as the corresponding phase id, which is a unique name of the CIF datablock and user will be able to modify it from GUI)
        * One or more datablocks (phases) in “pure cif” format according to the IUCr (International Union of Crystallography). Magnetic CIF (mcif) is currently not supported. We should keep mcif in mind, but get back to it once support of mcif is implemented into CrysPy or we bind another library which works with mcif. 
            * Unit cell parameters
            * Space group name and origin
            * List of atoms
            * Atomic coordinates and occupations
            * Atomic displacement parameters
        * Some custom parameters, such as local susceptibility tensor for polarised neutron diffraction. If/when they are accepted by the IUCr, this file would become a “pure cif”
    * Experiments directory with individual cif files for every experimental dataset (those files are named the same as the corresponding experimental dataset id)
        * One or more datablocks (experiments) as close as possible to the “pure cif” format
        * Experimental parameters required for the refinement, such as
            * Zero shift and wavelength
            * Instrumental resolution and peak asymmetry
            * Background, etc.
        * Other experimental metadata, which are not required for the refinement, but needed to better describe the experiment, such as,
            * Temperature, magnetic and electric field,
            * Facility, instrument name and its configuration name
            * Radiation type, experimental technique, etc.
            * Date and time of the measurements
            * Proposal DOI
        * Associated phase id with phase scale?
        * Measured data points (as columns), such as 2theta, intensity, sigma, etc.
    * Analysis.cif
        * Type of the calculator (cryspy, crysfml, …)
        * Minimization algorithm and related parameters (type of minimiser, maximum number of iterations, convergence criteria, etc.). Refinable parameters (model) are specified in Phases and Experiments.
        * The weighting scheme applied in the least-squares process. See, e.g., https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Irefine_ls_weighting_scheme.html 
    * Binding.cif
        * table to shows which phases are related to which experimental datasets 
        * a separate file, which would help to have a more clear structure. But it is also related with a position of this binding table in GUI (if it's a separate tab in GUI then a separate file is also more logical.)
    * Main.cif
        * Project name and keywords, which are specified by user when a new project is created from GUI. Both project name and keywords can be modified on the project handling tab.  Cif keys _samples and _experiments should be hardcoded, but not the directories with phase and experiments CIF files.
        * Links to other project cif files mentioned above. Currently, easyDiffraction supports only a single phase and single measured dataset. So, binding is done automatically. When we implement a support of multiple phases/files, an additional binding table should be created.  
* Internal application settings in a hidden folder:
    * Project description (converted from cif into python dictionary and saved as JSON?, as it is the closest format to the python dictionary).
        * Phases, including fitting information (which parameters are fitted, min, max, units).
        * Experiments, including fitting information (which parameters are fitted, min, max, units).
        * Simulation settings and refinement parameters. We could keep a track of all the intermediate steps in refinement process, so we could plot the changes of those parameters at any time.
        * Tooltips for all the parameters. Tooltip is a part of sub-dictionary which describes every parameter (along with its value, error, min and max, refine flag, etc.). If it's a experiment related parameter then it is stored as a part of experiment sub-dictionary of project dict. The same for phase related parameters. Fitting section just displays those parameters, which are related to the current experiment.  
        * URLs to for all the parameters
    * GUI
        * Application preferences (font, default instrument, plotting preferences, preferred output format...)
        * Window size and position
        * Currently opened tab
        * Folded/unfolded groups
        * Last opened folder of the project
    * Images
        * Crystal structure and simulation/analysis charts for the Home and Summary pages
    * History of changes for undo/redo
        * Project changes as saved by Qt Undo Framework (if possible)
        * GUI changes
        * Images changes
        * It's quite convenient to be able to undo/redo even after reloading the project, especially if you need to interrupt your current analysis but you can't leave application open until you can continue your work. Or if you decided to convert your previous work into python script. Therefore, an option to save project including undo/redo history should be implemented.  
    * Python script which would correspond to all the core commands done by user from GUI.
* Zip all the above into a single archive.  Zip file was used for simplicity, as it's more commonly supported compared to other formats. But, it's too easy to lose all the information when even a single bit is off, so possible alternatives should be considered, e.g., tar.
    * To compress project
    * To simplify handling and sharing (including SciCat)
