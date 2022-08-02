#骨干网拓扑
class Net:
    def __init__(self):
        self.network=[['Vancouver', 'LosAngeles', 'SanFrancisco', 'LasVegas', 'SaltLakeCity', 'ElPaso', 'Dallas', 'Houston',
                 'OklahomaCity', 'Minneapolis', 'KansasCity', 'Denver', 'Chicago', 'Indianapolis', 'Detroit', 'StLouis',
                 'Nashville', 'Cleveland', 'NewYork', 'Montreal', 'Charlotte', 'NewOrleans', 'Boston', 'Atlanta',
                 'Miami',
                 'WashingtonDC', 'Philadelphia', 'Toronto', 'Pittsburgh', 'Cincinnati', 'Tampa', 'Memphis', 'Winnipeg',
                 'Calgary', 'Seattle', 'Portland', 'Sacrameto', 'Phoenix', 'SanDiego'],[('Vancouver', 'Calgary'), ('Vancouver', 'Seattle'), ('LosAngeles', 'SanFrancisco'),
                 ('LosAngeles', 'LasVegas'),
                 ('LosAngeles', 'SanDiego'), ('SanFrancisco', 'LosAngeles'), ('SanFrancisco', 'Portland'),
                 ('SanFrancisco', 'Sacrameto'), ('LasVegas', 'LosAngeles'), ('LasVegas', 'SaltLakeCity'),
                 ('LasVegas', 'Sacrameto'), ('LasVegas', 'Phoenix'), ('SaltLakeCity', 'LasVegas'),
                 ('SaltLakeCity', 'Denver'),
                 ('SaltLakeCity', 'Calgary'), ('SaltLakeCity', 'Portland'), ('SaltLakeCity', 'Sacrameto'),
                 ('ElPaso', 'Dallas'),
                 ('ElPaso', 'Houston'), ('ElPaso', 'Phoenix'), ('Dallas', 'ElPaso'), ('Dallas', 'Houston'),
                 ('Dallas', 'OklahomaCity'), ('Dallas', 'Denver'), ('Dallas', 'Memphis'), ('Houston', 'ElPaso'),
                 ('Houston', 'Dallas'), ('Houston', 'NewOrleans'), ('OklahomaCity', 'Dallas'),
                 ('OklahomaCity', 'KansasCity'),
                 ('Minneapolis', 'KansasCity'), ('Minneapolis', 'Chicago'), ('Minneapolis', 'Winnipeg'),
                 ('KansasCity', 'OklahomaCity'), ('KansasCity', 'Minneapolis'), ('KansasCity', 'Denver'),
                 ('KansasCity', 'StLouis'), ('Denver', 'SaltLakeCity'), ('Denver', 'Dallas'), ('Denver', 'KansasCity'),
                 ('Chicago', 'Minneapolis'), ('Chicago', 'Indianapolis'), ('Chicago', 'Detroit'),
                 ('Chicago', 'StLouis'),
                 ('Indianapolis', 'Chicago'), ('Indianapolis', 'StLouis'), ('Indianapolis', 'Nashville'),
                 ('Indianapolis', 'Cincinnati'), ('Detroit', 'Chicago'), ('Detroit', 'Cleveland'),
                 ('Detroit', 'Toronto'),
                 ('StLouis', 'KansasCity'), ('StLouis', 'Chicago'), ('StLouis', 'Indianapolis'), ('StLouis', 'Memphis'),
                 ('Nashville', 'Indianapolis'), ('Nashville', 'Charlotte'), ('Nashville', 'Atlanta'),
                 ('Nashville', 'Memphis'),
                 ('Cleveland', 'Detroit'), ('Cleveland', 'NewYork'), ('Cleveland', 'Pittsburgh'),
                 ('Cleveland', 'Cincinnati'),
                 ('NewYork', 'Cleveland'), ('NewYork', 'Boston'), ('NewYork', 'Philadelphia'), ('NewYork', 'Toronto'),
                 ('Montreal', 'Boston'), ('Montreal', 'Toronto'), ('Charlotte', 'Nashville'), ('Charlotte', 'Atlanta'),
                 ('Charlotte', 'WashingtonDC'), ('Charlotte', 'Tampa'), ('NewOrleans', 'Houston'),
                 ('NewOrleans', 'Atlanta'),
                 ('NewOrleans', 'Miami'), ('NewOrleans', 'Memphis'), ('Boston', 'NewYork'), ('Boston', 'Montreal'),
                 ('Atlanta', 'Nashville'), ('Atlanta', 'Charlotte'), ('Atlanta', 'NewOrleans'), ('Atlanta', 'Tampa'),
                 ('Miami', 'NewOrleans'), ('Miami', 'Tampa'), ('WashingtonDC', 'Charlotte'),
                 ('WashingtonDC', 'Philadelphia'),
                 ('WashingtonDC', 'Pittsburgh'), ('Philadelphia', 'NewYork'), ('Philadelphia', 'WashingtonDC'),
                 ('Toronto', 'Detroit'), ('Toronto', 'NewYork'), ('Toronto', 'Montreal'), ('Pittsburgh', 'Cleveland'),
                 ('Pittsburgh', 'WashingtonDC'), ('Cincinnati', 'Indianapolis'), ('Cincinnati', 'Cleveland'),
                 ('Tampa', 'Charlotte'), ('Tampa', 'Atlanta'), ('Tampa', 'Miami'), ('Memphis', 'Dallas'),
                 ('Memphis', 'StLouis'), ('Memphis', 'Nashville'), ('Memphis', 'NewOrleans'),
                 ('Winnipeg', 'Minneapolis'),
                 ('Winnipeg', 'Calgary'), ('Calgary', 'Vancouver'), ('Calgary', 'SaltLakeCity'),
                 ('Calgary', 'Winnipeg'),
                 ('Seattle', 'Vancouver'), ('Seattle', 'Portland'), ('Portland', 'SanFrancisco'),
                 ('Portland', 'SaltLakeCity'),
                 ('Portland', 'Seattle'), ('Sacrameto', 'SanFrancisco'), ('Sacrameto', 'LasVegas'),
                 ('Sacrameto', 'SaltLakeCity'), ('Phoenix', 'LasVegas'), ('Phoenix', 'ElPaso'), ('Phoenix', 'SanDiego'),
                 ('SanDiego', 'LosAngeles'), ('SanDiego', 'Phoenix')]]

        self.leftset=[0,1,2,3,4,33,34,35,36,37,38]
        self.rightset=[5
,6
,7
,8
,9
,10
,11
,12
,13
,14
,15
,16
,17
,18
,19
,20
,21
,22
,23
,24
,25
,26
,27
,28
,29
,30
,31
,32
]