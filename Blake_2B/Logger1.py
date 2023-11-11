class Logger1(object):

    def __init__(self, filepath) -> None:
        self.file = open(filepath, "w")
    
    def log(self, data, tag, hierarchy=0, log=True):
        if log == False:
            return
        if type(data) == list:
            self.log("List Start", tag, hierarchy)
            for i in range(len(data)):
                temp = "[{index}]".format(index=i)
                self.log(temp + str(data[i]), "", hierarchy+1)
            self.log("", "List End", hierarchy)
            return
        else :
            tab = "\t" * hierarchy
            temp = tab + tag + ": " + str(data) + "\n";
            self.file.write(temp)
            return
        return

    def close(self):
        self.file.close()
        return
    pass




