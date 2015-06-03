clear all, close all

% Different likelihood and inference algorithms to choose
% id = [1,1]; % use Gauss/Exact
% id = [1,2; 3,2; 4,2]; % compare Laplace
% id = [1,3; 2,3; 3,3]; % study EP
% id = [1,5; 2,5]; % look into KL (takes quite a while)
% id = [1,4; 2,4; 3,4; 4,4]; % deal with VB
id = [1,4];

seed = 197; randn('seed',seed), rand('seed',seed)

% Preparing training set and test set
fprintf('Preparing dataset...\n')
load feature2;
load predict2;
total_size = size(feature);
ncount = total_size(1);
features = total_size(2);

% fraction of data used for training
trn_ratio = 0.8;

% number of training and test points
ntr = floor(ncount*trn_ratio); nte = ncount-ntr; 

xtr = feature(1:ntr,:);
ytr = predict(1:ntr,1);
xte = feature(ntr+1:ncount,:);
yte = predict(ntr+1:ncount,1);

% setup the GP
cov = {@covMaterniso,3}; sf = 1; ell = 0.4;
hyp0.cov  = log([ell;sf]);
likefunc = @likGauss;
sn = 0.1;
hyp0.lik = log(sn);

fprintf('Training and predicting...\n')
[ymu ys2 fmu fs2] = gp(hyp0, @infExact, [], cov, likefunc, xtr, ytr, xte);

fprintf('Computing mean squared error...\n')
sum(abs(yte-ymu).^2)/nte

fprintf('Computing one relative error...\n')
abs(yte(2)-ymu(2))/yte(2)
