clc; clear; close all

%% === Parámetros de ala y de simulación ===
P.N          = 29;        % Número de términos de Fourier
P.S          = 22;        % [m^2]
P.AR         = 7.5;       % Aspect ratio
P.lambda     = 0.55;      % Taper ratio
P.i_w        = 2;         % Ángulo de calaje del ala (deg)
P.a_2d       = 6.465;     % Pendiente 2D (1/rad)
P.alpha_0    = -3.75;     % Ángulo de 0 sustentación (deg)

% Rango de alpha_twist para el pre-cálculo
alpha_twist_range = -10:0.25:5;
num_steps = length(alpha_twist_range);

%% === Geometría básica (se calcula una sola vez) ===
P.deg2rad = pi/180;
P.b       = sqrt(P.AR * P.S);
P.c_root  = (1.5 * (1 + P.lambda) * (P.S / P.b)) / (1 + P.lambda + P.lambda^2);
P.theta   = (pi / (2 * P.N)) * (1:1:P.N);
P.z       = (P.b / 2) * cos(P.theta);
P.c       = P.c_root * (1 - (1 - P.lambda) * cos(P.theta));
P.mu      = (P.a_2d .* P.c) ./ (4 * P.b);

%% === Bucle de Pre-cálculo ===
fprintf('Iniciando pre-cálculo para %d valores de alpha_twist...\n', num_steps);
h_waitbar = waitbar(0, 'Pre-calculando distribuciones de sustentación...');
results(num_steps) = struct('alpha_twist', 0, 'CL_local', [], 'y_s', [], 'CL_wing', 0);
for k = 1:num_steps
    [results(k).CL_local, results(k).CL_wing, results(k).y_s] = calcularLift(alpha_twist_range(k), P);
    results(k).alpha_twist = alpha_twist_range(k);
    waitbar(k / num_steps, h_waitbar);
end
close(h_waitbar);
fprintf('Pre-cálculo completado.\n');

%% === Cálculo de la Referencia Elíptica FIJA (para alpha_twist = 0) ===
fprintf('Calculando referencia elíptica fija (para alpha_twist = 0°)...\n');
[~, CL_wing_ref, ~] = calcularLift(0, P); % CL del ala sin torsión
CL_root_ref = CL_wing_ref / (pi/4);
y_plot_ref = linspace(0, P.b/2, 100);
CL_elliptic_ref = CL_root_ref * sqrt(1 - (y_plot_ref / (P.b/2)).^2);
fprintf('Referencia elíptica generada con un CL_wing = %.4f.\n', CL_wing_ref);

%% === Creación de la interfaz gráfica ===
fig = uifigure('Name', 'Visualizador de Distribución de Sustentación', 'Position', [100 100 850 600]);
ax = uiaxes(fig, 'Position', [75 150 700 400]);
hold(ax, 'on');
grid(ax, 'on');
xlabel(ax, 'Posición en la semi-envergadura y (m)');
ylabel(ax, 'Coeficiente de sustentación local C_L(y)');

% 1. Dibujar la distribución elíptica de referencia (FIJA)
plot(ax, y_plot_ref, CL_elliptic_ref, 'r--', 'LineWidth', 2, 'DisplayName', 'Elíptica Fija (\alpha_{twist}=0°)');

% 2. Crear un objeto de línea para la distribución calculada, que se actualizará
h_plot_llt = plot(ax, NaN, NaN, '-o', 'LineWidth', 1.5, 'MarkerSize', 5, 'DisplayName', 'Calculada (LLT)');

legend(ax, 'Location', 'southwest');

% Slider para SELECCIONAR el índice del resultado
slider = uislider(fig, 'Position', [200 70 450 3], ...
    'Limits', [1, num_steps], ...
    'Value', find(alpha_twist_range == -3, 1), ...
    'MajorTicks', 1:num_steps);

uilabel(fig, 'Position', [375 90 200 22], 'Text', 'Seleccionar simulación');
valueLabel = uilabel(fig, 'Position', [390 40 150 22], 'HorizontalAlignment', 'center');

% Callback del slider: actualiza el plot y el título
slider.ValueChangedFcn = @(sld, event) updatePlot(sld, ax, valueLabel, h_plot_llt, results);

% Llamada inicial para dibujar la primera gráfica
updatePlot(slider, ax, valueLabel, h_plot_llt, results);

%% === Función para actualizar la gráfica (actualiza solo la curva azul) ===
function updatePlot(slider, ax, valueLabel, h_plot, results)
    idx = round(slider.Value);
    current_result = results(idx);
    
    % Actualizar los datos del objeto de la gráfica (más eficiente que cla)
    set(h_plot, 'XData', current_result.y_s, 'YData', current_result.CL_local);
    
    % Actualizar etiquetas y título
    valueLabel.Text = ['\alpha_{twist} = ' num2str(current_result.alpha_twist, '%.2f') '°'];
    title(ax, {['Distribución de Sustentación (Simulación ' num2str(idx) ')'], ...
               ['C_L_{ala} = ' num2str(current_result.CL_wing, '%.4f')]});
end

%% === Función de cálculo de LLT (sin cambios) ===
function [CL_s, CL_wing, y_s] = calcularLift(alpha_twist, P)
    alpha_geom = linspace(P.i_w + alpha_twist, P.i_w, P.N);
    LHS = P.mu .* ((alpha_geom - P.alpha_0) * P.deg2rad);
    B = zeros(P.N, P.N);
    for i = 1:P.N
        for j = 1:P.N
            n = 2*j - 1;
            B(i,j) = sin(n*P.theta(i)) * (1 + P.mu(i)*n/sin(P.theta(i)));
        end
    end
    A = B \ LHS(:);
    sum2 = zeros(1, P.N);
    for i = 1:P.N
        acc = 0;
        for j = 1:P.N
            n = 2*j - 1;
            acc = acc + A(j) * sin(n*P.theta(i));
        end
        sum2(i) = acc;
    end
    CL_local = (4*P.b .* sum2) ./ P.c;
    CL_wing = pi * P.AR * A(1);
    y_s  = [P.z, P.b/2];
    CL_s = [CL_local, 0];
end