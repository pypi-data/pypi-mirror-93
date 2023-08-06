# shinyutils
Various utilities for common tasks. :sparkles: :sparkles: :sparkles:

## Setup
Install with `pip`. Additional features can be enabled with the `[<feature>]` syntax shown below. Available optional features are:
* `color`: color support for logging and argument parsing
* `plotting`: support for `matplotlib` and `seaborn`
```bash
pip install shinyutils  # basic install
pip install "shinyutils[color]"  # install with color support
pip install "shinyutils[color,plotting]"  # install with color and plotting support
```

## Components

### `subcls`
Utility functions for dealing with subclasses.

#### Functions
* __`get_subclasses(cls)`__: returns a list of all the subclasses of `cls`.
* __`get_subclass_names(cls)`__: returns a list of names of all subclasses of `cls`.
* __`get_subclass_from_name(base_cls, cls_name)`__: return the subclass of `base_cls` named `cls_name`.

### `argp`
Utilities for argument parsing.

#### `LazyHelpFormatter`
`HelpFormatter` with sane defaults, and colors (courtesy of `crayons`)! To use, simply pass `formatter_class=LazyHelpFormatter` when creating `ArgumentParser` instances.
```python
arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
sub_parsers = arg_parser.add_subparsers(dest="cmd")
sub_parsers.required = True
# `formatter_class` needs to be set for sub parsers as well.
cmd1_parser = sub_parsers.add_parser("cmd1", formatter_class=LazyHelpFormatter)
```

#### `CommaSeparatedInts`
`ArgumentParser` type representing a list of `int` values. Accepts a string of comma separated values, e.g., `'1,2,3'`.

#### `InputFileType`
`FileType` restricted to input files, (with `'-'` for `stdin`). Returns a `file` object.

#### `OutputFileType`
`FileType` restricted to output files (with `'-'` for `stdout`). The file's parent directories are created if needed. Returns a `file` object.

#### `InputDirectoryType`
`ArgumentParser` type representing a directory. Returns a `Path` object.

#### `OutputDirectoryType`
`ArgumentParser` type representing an output directory. The directory is created if it doesn't exist. Returns a `Path` object.

#### `ClassType`
`ArgumentParser` type representing sub-classes of a given base class. The returned value is a `class`.
```python
class Base:
    pass

class A(Base):
    pass

class B(Base):
    pass

arg_parser.add_argument("--cls", type=ClassType(Base), default=A)
```

#### `KeyValuePairsType`
`ArgumentParser` type representing mappings. Accepts inputs of the form `str=val,[...]` where val is `int/float/str`. Returns a `dict`.

#### `shiny_arg_parser`
`ArgumentParser` object with `LazyHelpFormatter`, and arguments from sub-modules.

### `logng`
Utilities for logging.
#### `build_log_argp`
Creates an argument group with logging arguments.
```python
>>> arg_parser = ArgumentParser()
>>> _ = build_log_argp(arg_parser)  # returns the parser
>>> arg_parser.print_help()
usage: -c [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```
This function is called on `shiny_arg_parser` when `shinyutils` is imported.

#### `conf_logging`
Configures global logging using arguments returned by `ArgumentParser.parse_args`. `log_level` can be over-ridden with the keyword argument. Colors (enabled by default if `rich` is installed) can be toggled.
```python
args = arg_parser.parse_args()
conf_logging(args)
conf_logging(args, log_level="INFO")  # override `log_level`
conf_logging(use_colors=False)  # disable colors
```
When imported, `shinyutils` calls `conf_logging` without any arguments.

### `matwrap`
Wrapper around `matplotlib` and `seaborn`.

#### `MatWrap`
```python
from shinyutils.matwrap import MatWrap as mw  # do not import `matplotlib`, `seaborn`

mw.configure()  # this should be called before importing any packages that import matplotlib

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl()  # returns `matplotlib` module
mw.plt()  # returns `matplotlib.pyplot` module
mw.sns()  # returns `seaborn` module
```

Use `mw.configure` to configure plots. Arguments (defaults in bold) are:
* `context`: seaborn context (__paper__/poster/talk/notebook)
* `style`: seaborn style (white/whitegrid/dark/darkgrid/__ticks__)
* `font`: any font available to fontspec (default __Latin Modern Roman__)
* `latex_pkgs`: additional latex packages to be included before defaults
* `**rc_extra`: matplotlib rc parameters to override defaults
`mw.configure()` is called when `shinyutils.matwrap` is imported.

Use `add_parser_config_args` to add matwrap config options to an argument parser.
```python
>>> arg_parser = ArgumentParser()
>>> _ = mw.add_parser_config_args(arg_parser, group_title="plotting options")  # returns the parser group
>>> arg_parser.print_help()
usage: -c [-h] [--plotting-context {paper,notebook,talk,poster}]
          [--plotting-style {white,dark,whitegrid,darkgrid,ticks}]
          [--plotting-font PLOTTING_FONT]
          [--plotting-latex-pkgs PLOTTING_LATEX_PKGS [PLOTTING_LATEX_PKGS ...]]
          [--plotting-rc-extra PLOTTING_RC_EXTRA]

optional arguments:
  -h, --help            show this help message and exit

plotting options:
  --plotting-context {paper,notebook,talk,poster}
  --plotting-style {white,dark,whitegrid,darkgrid,ticks}
  --plotting-font PLOTTING_FONT
  --plotting-latex-pkgs PLOTTING_LATEX_PKGS [PLOTTING_LATEX_PKGS ...]
  --plotting-rc-extra PLOTTING_RC_EXTRA
```
`group_title` is optional, and if omitted, matwrap options will not be put in a separate group. When `shinyutils.matwrap` is imported, this function is called on `shiny_arg_parser`.

#### Plot
`Plot` is a wrapper around a single matplotlib plot, designed to be used as a context manager.
```python
from shinyutils.matwrap import Plot

with Plot(save_file, title, sizexy, labelxy, logxy) as ax:
  ...
```
Only the `save_file` argument is mandatory. When entering the context, `Plot` returns the plot axes, and when leaving, the plot is saved to the provided path.

### `pt`
Utilities for pytorch.

#### `PTOpt`
Wrapper around pytorch optimizer and learning rate scheduler.
```python
from shinyutils.pt import PTOpt
opt = PTOpt(
        weights,  # iterable of parameters to update
        optim_cls,  # subclass of torch.optim.Optimizer
        optim_params,  # arguments to initialize optim_cls
        lr_sched_cls,  # subclass of torch.optim.lr_scheduler._LRScheduler
        lr_sched_params,
)
...
opt.zero_grad()
loss.backward()
opt.step()
```
`lr_sched_` arguments are optional, and control the learning rate schedule. The class can also be used with argument parsers.
```python
>>> arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
>>> PTOpt.add_parser_args(
        arg_parser,
        arg_prefix="test",  # all options will be prefixed with "test-"
        group_title="pt test",  # if None, separate group will not be created
        default_optim_cls=Adam,
        default_optim_params=None,  # if None, default is an empty dict
        add_lr_decay=True,
    )
>>> arg_parser.print_help()
options:
  -h, --help                            show this help message and exit (optional)

pt test:
  --test-optim-cls cls                  ({Adadelta / Adagrad / Adam / AdamW / SparseAdam /
                                          Adamax / ASGD / SGD / Rprop / RMSprop / LBFGS}
                                          default: Adam)
  --test-optim-params str=val[,...]     (default: {})
  --test-lr-sched-cls cls               ({LambdaLR / MultiplicativeLR / StepLR / MultiStepLR /
                                        ExponentialLR / CosineAnnealingLR / CyclicLR /
                                        CosineAnnealingWarmRestarts / OneCycleLR} optional)
  --test-lr-sched-params str=val[,...]  (default: {})
>>> args = arg_parser.parse_args(...)
>>> opt = PTOpt.from_args(weights, args, arg_prefix="test")
```
`PTOpt` can also add help options to argument parsers to display signatures for optimizer and learning rate schedule classes.
```python
>>> arg_parser = ArgumentParser()
>>> PTOpt.add_help(arg_parser)
>>> arg_parser.print_help()
usage: -c [-h] [--explain-optimizer EXPLAIN_OPTIMIZER]
          [--explain-lr-sched EXPLAIN_LR_SCHED]

optional arguments:
  -h, --help            show this help message and exit

pytorch help:
  --explain-optimizer EXPLAIN_OPTIMIZER
                        describe arguments of a torch optimizer
  --explain-lr-sched EXPLAIN_LR_SCHED
                        describe arguments of a torch lr scheduler

>>> arg_parser.parse_args(["--explain-optimizer", "Adam"])
Adam(params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)
...
```
The help options are added to `shiny_arg_parser` when `shinyutils.pt` is imported.

#### `FCNet`
`FCNet` is a template class for fully connected networks.
```python
from shinyutils.pt import FCNet
net = FCNet(
        in_dim,  # input dimension
        out_dim,  # output dimension
        hidden_sizes,  # list of hidden layer sizes
        hidden_act,  # hidden layer activations (default relu)
        out_act,  # output layer activation (default None)
)
```
Like `PTOpt`, this class also supports construction through command line arguments.
```python
>>> arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
>>> FCNet.add_parser_args(
        arg_parser,
        arg_prefix="test",
        group_title="fcnet",
        default_indim=None,  # None means the option is mandatory
        default_outdim=1,
        default_hidden_sizes=None,
        default_hidden_act=F.relu,
        default_out_act=None,  # here, None means no output activation
)
>>> arg_parser.print_help()
options:
  -h, --help                           show this help message and exit (optional)

fcnet:
  --test-fcnet-indim int               (required)
  --test-fcnet-outdim int              (default: 1)
  --test-fcnet-hidden-sizes int,[...]  (required)
  --test-fcnet-hidden-act func         (default: relu)
  --test-fcnet-out-act func            (optional)
>>> args = arg_parser.parse_args(...)
>>> net = FCNet.from_args(args, arg_prefix="test")
```

#### `NNTrainer`
This class trains a model on a dataset, and accepts multiple dataset "formats".
```python
from shinyutils.pt import *
nn_trainer = NNTrainer(
    batch_size,  # only mandatory argument
    data_load_workers,  # default 0
    shuffle,  # default True
    pin_memory,  # default True
    drop_last,  # default True
    device,  # default cuda if available else cpu
)
nn_trainer.set_dataset(
    dataset,  # can be a torch Dataset, a tuple of torch Tensors, or a tuple of numpy arrays
)
model = FCNet(...)
opt = PTOpt(...)
loss_fn = torch.nn.functional.mse_loss
nn_trainer.train(model, opt, loss_fn, iters)
```

#### `SetTBWriterAction`
`argparse` action to create a tensorboard summary writer. The writer is stored in the `tb_writer` attribute of the argument namespace; this can be overridden by setting `SetTBWriterAction.attr`. The usage is shown below with the tensorboard option that is added to `shiny_arg_parser` on importing the module.
```python
shiny_arg_parser.add_argument(
    "--tb-dir",
    type=OutputDirectoryType(),
    help="tensorboard log directory",
    default=None,
    action=SetTBWriterAction,
)
shiny_arg_parser.set_defaults(**{SetTBWriterAction.attr: Mock(SummaryWriter)})
```
`shiny_arg_parser.tb_writer` will contain a `SummaryWriter` like object. If no log directory is provided through the command line, this object will be a dummy. So tensorboard functions can be called on the writer without extra checks.
