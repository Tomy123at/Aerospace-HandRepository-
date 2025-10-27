clc; clear; close all

%% === Parámetros de ala (Editables) ===
N          = 29;       % número de términos/slices (Fourier odd terms) - Aumentado para más precisión
S          = 22;       % [m^2]
AR         = 7.5;      % Aspect ratio
lambda     = 0.55;     % taper ratio = C_tip / C_root
i_w        = 2;        % ángulo de calaje del ala (deg)
a_2d       = 6.465;    % pendiente 2D (1/rad)
alpha_0    = -3.75;    % ángulo de 0 sustentación (deg)

%% === Geometría básica (No se modifica en el bucle) ===
deg2rad = pi/180;
b       = sqrt(AR*S);         % envergadura [m]
MAC     = S/b;                % cuerda media aerodinámica
Croot   = (1.5*(1+lambda)*MAC)/(1 + lambda + lambda^2); % cuerda root
theta   = (pi/(2*N))*(1:1:N);   % N puntos entre (pi/2N) y (pi/2)
z       = (b/2)*cos(theta);     % y local (semi-ala, de ~b/2 a 0)
c       = Croot*(1 - (1 - lambda)*cos(theta)); % cuerda local en cada theta

%% === Creación de la interfaz gráfica ===
fig = uifigure('Name', 'Ajuste de Distribución de Sustentación', 'Position', [100 100 800 600]);
ax = uiaxes(fig, 'Position', [50 150 700 400]);
grid(ax, 'on');
xlabel(ax, 'Semi-span location y (m)');
ylabel(ax, 'Local C_L(y)');
title(ax, 'Distribución de Sustentación (Lifting-Line)');
hold(ax, 'on'); % Mantener las gráficas

% Slider para alpha_twist
slider = uislider(fig, 'Position', [150 50 500 3], 'Limits', [-10, 5], 'Value', -3);
label = uilabel(fig, 'Position', [350 70 200 22], 'Text', 'Ajustar Alpha Twist (deg)');
valueLabel = uilabel(fig, 'Position', [670 45 100 22], 'Text', ['Valor: ' num2str(slider.Value, '%.2f')]);

% Añadir un listener para el evento 'ValueChanged' del slider
slider.ValueChangedFcn = @(sld, event) updatePlot(sld, event, ax, valueLabel, N, S, AR, lambda, i_w, a_2d, alpha_0, b, Croot, theta, z, c, deg2rad);

% Llamada inicial para dibujar la primera gráfica
updatePlot(slider, [], ax, valueLabel, N, S, AR, lambda, i_w, a_2d, alpha_0, b, Croot, theta, z, c, deg2rad);


%% === Función de actualización y cálculo ===
function updatePlot(slider, event, ax, valueLabel, N, S, AR, lambda, i_w, a_2d, alpha_0, b, Croot, theta, z, c, deg2rad)
    % Obtener el valor actual del slider
    alpha_twist = slider.Value;
    
    % Actualizar la etiqueta del valor
    valueLabel.Text = ['Valor: ' num2str(alpha_twist, '%.2f')];
    
    % --- INICIO CÁLCULOS DE LIFTING-LINE (como en tu script original) ---
    
    % Distribución de ángulo de ataque geométrico
    alpha_geom = linspace(i_w + alpha_twist, i_w, N); % [deg]
    
    % Parámetro mu_i
    mu = (a_2d .* c) ./ (4*b);
    
    % Lado izquierdo del sistema (en rad)
    LHS = mu .* ((alpha_geom - alpha_0) * deg2rad);
    
    % Construcción de la matriz B
    B = zeros(N,N);
    for i = 1:N
        for j = 1:N
            n = 2*j - 1;
            B(i,j) = sin(n*theta(i)) * (1 + mu(i)*n/sin(theta(i)));
        end
    end
    
    % Resolver coeficientes de Fourier
    A = B \ LHS(:);
    
    % Recuperar distribución de CL local
    sum2 = zeros(1,N);
    for i = 1:N
        acc = 0;
        for j = 1:N
            n = 2*j - 1;
            acc = acc + A(j)*sin(n*theta(i));
        end
        sum2(i) = acc;
    end
    CL_local = (4*b .* sum2) ./ c;
    
    % CL total del ala
    CL_wing = pi * AR * A(1);
    
    % --- FIN CÁLCULOS DE LIFTING-LINE ---

    % --- CÁLCULO DE LA DISTRIBUCIÓN ELÍPTICA DE REFERENCIA ---
    % La distribución elíptica tiene la forma de una semi-elipse.
    % CL_local(y) = CL_root * sqrt(1 - (y / (b/2))^2)
    % Para que tenga el mismo área (misma sustentación total), igualamos CL_wing
    % CL_wing_elliptic = integral de CL_local(y)*c(y) / S
    % Para una distribución elíptica pura, CL_root = (4 * CL_wing) / (pi * AR * c(0)/b)
    % Una forma más simple es escalar la forma elíptica para que el CL total coincida.
    % CL_root_ref = (4 * CL_wing) / pi; % CL en el centro para una dist. elíptica con CL_wing
    CL_root_ref = CL_wing / (pi/4); % Forma estándar: CL_wing = CL_root * pi/4
    y_plot_full = linspace(0, b/2, 100); % Vector de y para una gráfica suave
    CL_elliptic = CL_root_ref * sqrt(1 - (y_plot_full / (b/2)).^2);
    
    
    % --- ACTUALIZACIÓN DE LA GRÁFICA ---
    cla(ax); % Limpiar los ejes antes de volver a dibujar
    
    % Graficar la distribución elíptica (fija para un CL_wing dado)
    plot(ax, y_plot_full, CL_elliptic, 'r--', 'LineWidth', 2, 'DisplayName', 'Distribución Elíptica Ideal');
    
    % Preparar datos para graficar incluyendo la punta (y=b/2, CL=0)
    y_s  = [z, b/2]; % y va de 0 a b/2
    CL_s = [CL_local, 0]; % CL en la punta es 0
    
    % Graficar la distribución calculada
    plot(ax, y_s, CL_s, '-o', 'LineWidth', 1.5, 'MarkerSize', 5, 'DisplayName', 'Distribución Calculada (LLT)');
    
    % Actualizar título y leyenda
    title(ax, {['Distribución de Sustentación para \alpha_{twist} = ' num2str(alpha_twist, '%.2f') ' deg'], ...
               ['C_L (total) = ' num2str(CL_wing, '%.4f')]});
    legend(ax, 'Location', 'southwest');
    ylim(ax, [0, max(CL_elliptic)*1.2]); % Ajustar el límite Y para que todo sea visible
    hold(ax, 'off');
end