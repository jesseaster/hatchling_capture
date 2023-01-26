import csv
import glob
import os


class LoadProject:
    def getProjects(self):
        txtfiles = []
        for file in glob.glob("*.csv"):
            txtfiles.append(file)
        return txtfiles

    def loadProject(self, csvfilename):
        with open(csvfilename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='\'')
            for row in spamreader:
                print(', '.join(row))

    def saveData(self, csvfilename, variables):
        with open(csvfilename, 'a', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile,
                delimiter=",",
                quotechar='\'',
                quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([variables[0],
                                variables[1],
                                variables[2],
                                variables[3]])

    def newProject(self, projectName):
        csvfilename = projectName + '.csv'
        path = os.getcwd()
        path = path + "\\" + projectName

        # If path does not exist, create it
        if not os.path.isdir(path):
            os.mkdir(path)

        with open(csvfilename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile,
                delimiter=",",
                quotechar='\'',
                quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Experiment Name',
                                 'ID',
                                 'DateTime',
                                 'Image',
                                 ])


if __name__ == '__main__':
    lp = LoadProject()

    txtfiles = lp.getProjects()
    if len(txtfiles) > 0:
        csvfilename = txtfiles[0]
        variables = [
            "Project1",
            "3.0",
            "01-26-2023 18.14",
            "Project1\\01-26-2023.18.14_3.0.png"]
        lp.loadProject(csvfilename)
        lp.saveData(csvfilename, variables)
        lp.loadProject(csvfilename)
