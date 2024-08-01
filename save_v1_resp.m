% Define directories
input_dir = 'outputs/mat/';
output_dir = 'v1_response/';

% Create the output directory if it does not exist
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

% Get a list of all .mat files in the input directory
mat_files = dir(fullfile(input_dir, '*.mat'));

% Load the trained model (assuming it's the same for all images)
load('model_trained_in_Lshape.mat', 'env', 'lgn', 'v1', 'v1_response_max', 'lca');

% Loop through each .mat file
for k = 1:length(mat_files)
    % Get the current file name and index
    [~, name, ~] = fileparts(mat_files(k).name);
    indx = name; % Assuming the name contains the index

    % Load the image data from the .mat file
    mat_file_path = fullfile(input_dir, mat_files(k).name);
    load(mat_file_path, 'images_data');
    img = images_data;
    img = double(img) / 255;

    % Process the image
    img = reshape(img, env.fov_x, env.fov_y)';
    lgn_response = lgn_processing(img, lgn);
    [~, v1_response] = v1_processing(lgn_response, v1);
    v1_response = v1_response / v1_response_max; % response scaled by a global factor

    % Plot the result
    figure();
    imagesc(imresize(reshape(v1_response, v1.num_complex*v1.Nx, v1.Ny)', [v1.Ny v1.Nx]));
    colormap(gca, 'gray');

    % Save the plot
    output_file_path = fullfile(output_dir, ['plot_' indx '.png']);
    saveas(gcf, output_file_path);

    % Close the figure to save memory
    close(gcf);
end
