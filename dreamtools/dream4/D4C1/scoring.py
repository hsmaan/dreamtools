
import os
import StringIO
from dreamtools.core.challenge import Challenge

import pandas as pd
class D4C1(Challenge):
    """A class dedicated to D4C1 challenge

    ::

        from dreamtools import D4C1
        s = D4C1()
        filename = s.download_template() 
        s.score(filename) 

    Data and templates are downloaded from Synapse. You must have a login.

    """
    def __init__(self):
        """.. rubric:: constructor

        """
        super(D4C1, self).__init__('D4C1')
        self._path2data = os.path.split(os.path.abspath(__file__))[0]

        self._load_golddata()

    def score(self, prediction_file):
        raise NotImplementedError

    def read_section(self):
        pass

    def _load_golddata(self):
        filename = self._pj([self._path2data, 'goldstandard', 'D4C1_goldstandard.txt'])
        data = open(filename).read()
        # in principle, the file contains 13 matrices with an empty line in between (hence the
        # \n\n and there is a line before each matrix that is not a header hence header=None
        self.golddata = []
        for i in range(0,13):
            df = pd.read_csv(StringIO.StringIO(data.split("\n\n")[0]), header=None, sep='\t', 
                skiprows=1, index_col=0)
            assert all(df.sum() == [1]*10), 'sum over a column must be equal to 1'
            self.golddata.append(df)

    def _load_prediction(self, filename):
        data = open(filename).read()
        # in principle, the file contains 13 matrices with an empty line in between (hence the
        # \n\n and there is a line before each matrix that is not a header hence header=None
        self.prediction = []
        for i in range(0,13):
            df = pd.read_csv(StringIO.StringIO(data.split("\n\n")[0]), header=None, sep='\t', 
                skiprows=1, index_col=0)
            if all(df.apply(lambda x: abs(x.sum()-1)<1e-12)) is False:
                print all(df.apply(lambda x: abs(x.sum()-1)<1e-12))
                print('In Matrix %s, the sum over a column is not equal to 1!!' % (i+1))
                print df.sum()
                raise ValueError
            self.prediction.append(df)

    def download_template(self):
        filename = self._pj([self._path2data, 'templates', 'D4C1_templates.txt'])
        return filename



"""
% This function produces the DREAM4 scores for Challenge 1.
%
% See go.m for an example of how to call it.
%
% Gustavo A. Stolovitzky, Ph.D.
% Adj. Assoc Prof of Biomed Informatics, Columbia Univ
% Mngr, Func Genomics & Sys Biology, IBM  Research
% P.O.Box 218 					Office :  (914) 945-1292
% Yorktown Heights, NY 10598 	Fax     :  (914) 945-4217
% http://www.research.ibm.com/people/g/gustavo
% http://domino.research.ibm.com/comm/research_projects.nsf/pages/fungen.index.html 
% gustavo@us.ibm.com
%
% Robert Prill, Ph.D.
% Postdoctoral Researcher
% Computational Biology Center, IBM Research
% P.O.Box 218
% Yorktown Heights, NY 10598 	
% Office :  914-945-1377
% http://domino.research.ibm.com/comm/research_people.nsf/pages/rjprill.index.html
% rjprill@us.ibm.com
%

function [kinase, pdz, sh3] = DREAM4_Challenge1_Evaluation(DATADIR,GOLDDIR,PDFDIR)
%% returns three structures 

%% indices of the three sub-challenges
%idx_sh3 = 1:5;
%idx_sh3 = [1 2 3];		%% what was available as of the conference
idx_sh3 = [1 2 3 5];	%% we're still waiting for gold std #4
idx_kinase = 6:8;
idx_pdz = 9:13;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% load gold standard (3D matrix)
gold = load_matrices(GOLDDIR);

%% load prediction (3D matrix)
prediction = load_matrices(DATADIR);
	
%% distance from gold (3D matrix)
D = gold - prediction;

%% summary table of scores
F = frobenius_norm_3d(D);


%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% kinase sub-challenge
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for ii = 1:length(idx_kinase)
	idx = idx_kinase(ii);
	
	%% load and unpack probability density function
	pdffile = [ PDFDIR 'pdf_' num2str(idx) ];
	d = load(pdffile);
	h = d.h;
	x = d.x;
	X = d.X;
	Y = d.Y;
	C = d.C;
	
	mydist = F(idx);
	pval = probability(X,Y,mydist);
	
	%% cap pvals at 1e-100 since the precision is limited
	if pval < 1e-100
		pval = 1e-100
	end

	%% remember
	mydists(ii) = mydist;
	pvals(ii) = pval;
	
end

overall = -mean(log10(pvals));

%% pack-up
kinase.overall_score = overall;
kinase.pvals = pvals;
kinase.distances = mydists;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PDZ sub-challenge
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for ii = 1:length(idx_pdz)
	idx = idx_pdz(ii);
	
	%% load and unpack probability density function
	pdffile = [ PDFDIR 'pdf_' num2str(idx) ];
	d = load(pdffile);
	h = d.h;
	x = d.x;
	X = d.X;
	Y = d.Y;
	C = d.C;
	
	mydist = F(idx);
	pval = probability(X,Y,mydist);
	
	%% cap pvals at 1e-100 since the precision is limited
	if pval < 1e-100
		pval = 1e-100;
	end

	%% remember
	mydists(ii) = mydist;
	pvals(ii) = pval;
	
end

overall = -mean(log10(pvals));

%% pack-up
pdz.overall_score = overall;
pdz.pvals = pvals;
pdz.distances = mydists;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% SH3 sub-challenge
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for ii = 1:length(idx_sh3)
	idx = idx_sh3(ii);

	%% load and unpack probability density function
	pdffile = [ PDFDIR 'pdf_' num2str(idx) ];
	d = load(pdffile);
	XX = d.XX;
	YY = d.YY;

	%% slide T relative to G
	G = gold(:,:,idx);
	T = prediction(:,:,idx);
	[ scores offsets ] = slide(G,T);

	%% for each offset, get the pval
	for jj = 1:length(offsets)
		score = scores(jj);
		X = XX(:,jj);
		Y = YY(:,jj);
		pval = probability(X,Y,score);
		
		%% cap pvals at 1e-100 since the precision is limited
		if pval < 1e-100
			pval = 1e-100
		end

		%% remember
		pvals(jj) = pval;
	end

	%% take the best pval
	pval_best = min(pvals);
	idx_best = find([pvals==pval_best]);
	offset_best = offsets(idx_best);

	%% remember
	PVAL(ii) = pval_best;
	OFFSET(ii) = offset_best;
	
end

overall = -mean(log10(PVAL));

%% pack-up
sh3.overall_score = overall;
sh3.pvals = PVAL;
sh3.offsets = OFFSET;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function F = frobenius_norm_3d(X)

%% Frobenius Norm
%% http://mathworld.wolfram.com/FrobeniusNorm.html

for ii = 1:size(X,3)

	%% unpack
	x = X(:,:,ii);

    %% Frobenius:1

	f = sqrt(sum(diag(x * x')));

	%% remember
	F(ii) = f;

end
%
% Gustavo A. Stolovitzky, Ph.D.
% Robert Prill, Ph.D.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [score offset] = slide(G,T)

count = 0;

%% slide T relative to G
t_stop = 10;
g_start = 1;
for t_start = 6:-1:1
	g_stop = 10 - t_start + 1;

	idx_t = t_start:t_stop;
	idx_g = g_start:g_stop;

	g = G(:,idx_g);
	t = T(:,idx_t);
	
	%% matrix of element distances
	d = g - t;

	%% frob norm
	f = frobenius_norm_3d(d);
	
	%% number of overlapping rows
	overlap = length(idx_t);

	%% remember realtive position
	count = count + 1;
	offset(count) = g_start - t_start;

	%% remember score
%	score(count) = f / overlap;
	score(count) = f;

end
%% last position is complete overlap

%% continue sliding T relative to G
t_start = 1;
g_stop = 10;
for t_stop = 9:-1:5
	g_start = 10 - t_stop + 1;
	
	idx_t = t_start:t_stop;
	idx_g = g_start:g_stop;

	g = G(:,idx_g);
	t = T(:,idx_t);
	
	%% matrix of element distances
	d = g - t;

	%% frob norm
	f = frobenius_norm_3d(d);
	
	%% number of overlapping rows
	overlap = length(idx_t);

	%% remember realtive position
	count = count + 1;
	offset(count) = g_start - t_start;

	%% remember score
%	score(count) = f / overlap;
	score(count) = f;
	
end
"""
