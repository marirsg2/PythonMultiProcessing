import multiprocessing as mp

#create a forkserver
#have pipes to pass a python object

class dummy_data_holder_class:

    def __init__(self):
        self.data_holder = "init"

    def __del__(self):
        pass

    def read_data(self):
        return self.data_holder

    def write_data(self,new_data):
        self.data_holder = new_data



def process_function_handler(pipe_handle):
    #will receive the object piped in. Check if python does a blocking wait or non-blocking wait
    recv_py_obj = pipe_handle.recv()
    print(recv_py_obj)
    # will print information in the object
    print(recv_py_obj.read_data())
    #modify information, and send it back to be checked
    recv_py_obj.write_data("modified by auxilliary process")
    pipe_handle.send(recv_py_obj)

if __name__ == "__main__":
    mp.set_start_method('forkserver')
    main_pipe_handle,aux_pipe_hanlde = mp.Pipe()
    #todo IMPORTANT TO READ, the args if only one argument HAS to be (xyz, ). The last comma makes it an iterable
    aux_process = mp.Process(target=process_function_handler, args = (aux_pipe_hanlde,))
    aux_process.start()
    py_object = dummy_data_holder_class()
    py_object.write_data("modified by main process")
    print(py_object)
    main_pipe_handle.send(py_object)
    msg = main_pipe_handle.recv()
    aux_process.join()
    print(msg)
    print(msg.read_data())
    print("END of Parallel process testing")
