clc; clear; close all

%% === Parámetros de ala ===
N          = 9;        % número de términos/slices (Fourier odd terms)
S          = 22;       % [m^2]
AR         = 7.5;        % Aspect ratio
lambda     = 0.55;      % taper ratio = C_tip / C_root
alpha_twist= -1.5;       % twist lineal (deg) (tip respecto a root)
i_w        = 2.55;        % ángulo de calaje del ala (deg)
a_2d       = 6.465;      % pendiente 2D (1/rad)
alpha_0    = -3.75;     % ángulo de 0 sustentación (deg)

deg2rad = pi/180;

%% === Geometría básica ===
b    = sqrt(AR*S);          % envergadura [m]
MAC  = S/(b);             % chord medio aerodinámico S/(b/2) = 2S/b
Croot= (1.5*(1+lambda)*MAC)/(1 + lambda + lambda^2);  % cuerda root

% Ángulos collocation (Método de Multhopp/Prandtl)
theta = (pi/(2*N))*(1:1:N);           % N puntos entre (pi/2N) y (pi/2)
z     = (b/2)*cos(theta);             % y local (semi-ala, de ~b/2 a 0)
c     = Croot*(1 - (1 - lambda)*cos(theta));   % cuerda local en cada theta

% Distribución de ángulo de ataque geométrico (calaje + twist lineal)
% i_w en el root y i_w+alpha_twist en el tip (o viceversa según signo)
alpha_geom = linspace(i_w + alpha_twist, i_w, N);   % [deg]

% Parámetro mu_i = a2D * c_i / (4b)
mu = (a_2d .* c) ./ (4*b);

%% === Lado izquierdo del sistema (en rad) ===
% α_eff = α_geom - α_0 (en deg) -> convertir a rad
LHS = mu .* ((alpha_geom - alpha_0) * deg2rad);   % vector 1xN

%% === Construcción de la matriz B (N×N) ===
B = zeros(N,N);
for i = 1:N
    for j = 1:N
        n     = 2*j - 1;  % armónicos impares
        B(i,j)= sin(n*theta(i)) * ( 1 + mu(i)*n/sin(theta(i)) );
    end
end

%% === Resolver coeficientes de Fourier A_j ===
A = B \ LHS(:);   % A es Nx1, con A1, A3, A5, ...

%% === Recuperar distribución de CL local ===
% sum2_i = sum_j A_j * sin((2j-1)*theta_i)
sum2 = zeros(1,N);
for i = 1:N
    acc = 0;
    for j = 1:N
        n   = 2*j - 1;
        acc = acc + A(j)*sin(n*theta(i));
    end
    sum2(i) = acc;
end

% CL(y) = (4b/c(y)) * sum2_i
CL_local = (4*b .* sum2) ./ c;

%% === Preparar datos para graficar incluyendo punta (y=b/2, CL=0) ===
y_s  = [b/2, z];          % poner primero la punta exacta y=b/2
CL_s = [0,   CL_local];   % en la punta CL=0

%% === Gráfica ===
figure
plot(y_s, CL_s, '-o', 'LineWidth', 1.5, 'MarkerSize', 6)
grid on
xlabel('Semi-span location y (m)')
ylabel('Local C_L(y)')
title('Lift distribution (lifting-line)')

%% === CL del ala (coeficiente total) ===
CL_wing = pi * AR * A(1);   % A1 es el primer coeficiente impar
fprintf('C_L (wing) = %.5f\n', CL_wing);
