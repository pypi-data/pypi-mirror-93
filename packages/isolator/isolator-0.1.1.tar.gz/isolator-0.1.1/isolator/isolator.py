"""Utility class to isolate a class into a separate process.

The isolator can be used to segregate the instantiation and execution of a
class into a separte process.
"""
from multiprocessing import Process, Queue
import signal
import os


# The SIGINT gets turned into a keyboard interrupt exception as default in
# python, which will not necesarily clean up the Isolator process.
# Turning SIGINT into SIGTERM makes the Isolator shut down in these situations
# (along with the main process), because Isolator is a daemon.
def terminate(*_):
    """Issue a SIGTERM signal to the current process."""
    os.kill(os.getpid(), signal.SIGTERM)


signal.signal(signal.SIGINT, terminate)


class AlreadyProcessing(Exception):
    """Raised when an Isolator is already processing something."""


class Isolator(Process):
    """A utility class to isolate model execution in a separate process.

    Before being able to properly use the Isolator, some methods of the
    isolated model have to be exposed by calling the `Isolator.register_call()`
    method. Consider using the `Isolator.isolate()` classmethod for a complete
    single-call setup.

    Parameters
    ----------
    model_class
        The model class to instantiate.
    exposed_methods: list of str
        The names of methods of the isolated model to expose
    model_args: tuple
        The positional arguments to use when instantiating the model.
    model_kwargs: dict
        The keyword arguments to use when instantiating the model.
    kwargs
        Keyword arguments are forwareded to the Process base class.

    """

    def __init__(self,
                 model_class,
                 model_args=None,
                 model_kwargs=None,
                 **kwargs
                 ):
        """Instantiate a new Isolator."""
        super().__init__(**kwargs)

        self.model_class = model_class
        self.model_args = model_args or ()
        self.model_kwargs = model_kwargs or {}

        self.in_queue = Queue(maxsize=1)
        self.out_queue = Queue()
        self.daemon = True

        self.__is_processing = False

        self.start()

    @classmethod
    def isolate(cls,
                model_class,
                exposed_methods,
                model_args=None,
                model_kwargs=None,
                **kwargs):
        """Set up an Isolator instance and expose some model methods.

        This classmethod bundles the __init__ of an Isolator with the exposing
        of some of the model methods.

        Parameters
        ----------
        model_class
            The model class to instantiate.
        exposed_methods: list of str
            The names of methods of the isolated model to expose
        model_args: tuple
            The positional arguments to use when instantiating the model.
        model_kwargs: dict
            The keyword arguments to use when instantiating the model.
        kwargs
            Keyword arguments are forwareded to the Process base class.

        """
        isolated = cls(model_class=model_class,
                       model_args=model_args,
                       model_kwargs=model_kwargs,
                       **kwargs)
        for method in exposed_methods:
            isolated.register_call(method)
        return isolated

    def register_call(self, func_name, overwrite=False):
        """Expose a model method.

        Running self.register_call will add a method to this object that
        executes the model's corresponding method in a different process.

        Parameters
        ----------
        func_name: str
            The name of the method to expose.
        overwrite: bool
            Whether overwriting an exisitng attribute is ok.

        """
        if not overwrite and hasattr(self, func_name):
            raise ValueError(
                f"An attribute of name '{func_name}' already exists")

        def wrapped(*args, **kwargs):
            # Could not get it to work with Lock.aquire(block=False)
            if self.__is_processing:
                raise AlreadyProcessing
            try:
                self.__is_processing = True
                self.in_queue.put_nowait((func_name, args, kwargs))
                result = self.out_queue.get()
                if isinstance(result, Exception):
                    raise result
                else:
                    return result
            finally:
                self.__is_processing = False

        setattr(self, func_name, wrapped)

    def run(self):
        """Run the isolated process.

        This method automatically gets called by self.start().

        """
        self.model = self.model_class(*self.model_args, **self.model_kwargs)

        for dispatch, args, kwargs in iter(self.in_queue.get, "STOP"):
            try:
                result = getattr(self.model, dispatch)(*args, **kwargs)
            except Exception as e:
                result = e

            self.out_queue.put(result, block=True)

    def __del__(self):
        """Clean up when deleting this object."""
        self.in_queue.put("STOP")
        self.join()
