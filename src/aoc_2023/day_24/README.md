# AoC 2023 Day 24

**Input:** $(x_i, y_i, z_i, Vx_i, Vy_i, Vz_i)\,\forall i \in [1,...,n]$

**Goal:** Find $(x_R, y_R, z_R, Vx_R, Vy_R, Vz_R)$ that intersects with every input line.

----

$(x_i, y_i, z_i, Vx_i, Vy_i, Vz_i)$ intersects with $(x_R, y_R, z_R, Vx_R, Vy_R, Vz_R)$

$\implies$ $\exists t \in \N_{\ge 0}$ s.t.
$$
x_i + t \cdot Vx_i = x_R + t \cdot Vx_R, \\
y_i + t \cdot Vy_i = y_R + t \cdot Vy_R \\
\text{and } z_i + t \cdot Vz_i = z_R + t \cdot Vz_R. \\
$$

$\implies \exists t \in \N_{\ge 0}$ s.t.
$$
t = \frac{-(x_R - x_i)}{Vx_R - Vx_i} = \frac{-(y_R - y_i)}{Vy_R - Vy_i} = \frac{-(z_R - z_i)}{Vz_R - Vz_i}
$$

$\implies$
$$
(x_R - x_i)(Vy_R - Vy_i) - (y_R - y_i)(Vx_R - Vx_i) = 0 \\
\text{and } (x_R - x_i)(Vz_R - Vz_i) - (z_R - z_i)(Vz_R - Vz_i) = 0.
$$

If we consider $i \neq j \in [1,...,n]$,

$$(x_R - x_i)(Vy_R - Vy_i) - (y_R - y_i)(Vx_R - Vx_i) = 0 \tag{1}$$
$$(x_R - x_j)(Vy_R - Vy_j) - (y_R - y_j)(Vx_R - Vx_j) = 0 \tag{2}$$
$$(x_R - x_i)(Vz_R - Vz_i) - (z_R - z_i)(Vz_R - Vz_i) = 0 \tag{3}$$
$$(x_R - x_j)(Vz_R - Vz_j) - (z_R - z_j)(Vz_R - Vz_j) = 0 \tag{4}$$

Subtracting equation (2) from equation (1) yields
$$
\begin{aligned}
&(x_R - x_i)(Vy_R - Vy_i) - (y_R - y_i)(Vx_R - Vx_i) \\
- &(x_R - x_j)(Vy_R - Vy_j) + (y_R - y_j)(Vx_R - Vx_j) = 0
\end{aligned}
$$

$$
\begin{aligned}
&x_R(Vy_R - Vy_i) - x_i(Vy_R - Vy_i) - y_R(Vx_R - Vx_i) + y_i(Vx_R - Vx_i) \\
- &x_R(Vy_R - Vy_j) + x_j(Vy_R - Vy_j) + y_R(Vx_R - Vx_j) - y_j(Vx_R - Vx_j) = 0
\end{aligned}
$$

$$
x_R(- Vy_i + Vy_j) + y_R(Vx_i - Vx_j) + Vx_R (y_i - y_j) + Vy_R (-x_i + x_j) \\
+ x_i \cdot Vy_i - y_i \cdot Vx_i - x_j \cdot Vy_j + y_j \cdot Vx_j = 0
$$

$$
\begin{pmatrix}
-Vy_i + Vy_j \\
Vx_i - Vx_j \\
0 \\
y_i - y_j \\
-x_i + x_j \\
0
\end{pmatrix} ^T \cdot \begin{pmatrix}
x_R \\
y_R \\
z_R \\
Vx_R \\
Vy_R \\
Vz_R
\end{pmatrix}
= -(x_i \cdot Vy_i - y_i \cdot Vx_i - x_j \cdot Vy_j + y_j \cdot Vx_j)
$$

Similarly, subtracting equation (4) from equation (3) yields
$$
x_R(- Vz_i + Vz_j) + z_R(Vx_i - Vx_j) + Vx_R (z_i - z_j) + Vz_R (-x_i + x_j) \\
+ x_i \cdot Vz_i - z_i \cdot Vx_i - x_j \cdot Vz_j + z_j \cdot Vx_j = 0
$$

$$
\begin{pmatrix}
-Vz_i + Vz_j \\
0 \\
Vx_i - Vx_j \\
z_i - z_j \\
0 \\
-x_i + x_j
\end{pmatrix} ^T \cdot \begin{pmatrix}
x_R \\
y_R \\
z_R \\
Vx_R \\
Vy_R \\
Vz_R
\end{pmatrix} = -(x_i \cdot Vz_i - z_i \cdot Vx_i - x_j \cdot Vz_j + z_j \cdot Vx_j)
$$

We need 6 equations to solve for the 6 unknowns. Since each pair of input lines $i \neq j$ yields 2 equations, we need $\frac{6}{2} = 3$ such pairs. We can arbitrarily select the following: $(i, j) \in [(1, 2), (2, 3), (3, 4)]$.

Thus, $x :=(x_R, y_R, z_R, Vx_R, Vy_R, Vz_R)$ is the solution to the system of equations $Ax = b$, where:

$$
A := \begin{pmatrix}
-Vy_1 + Vy_2 & Vx_1 - Vx_2 & 0 & y_1 - y_2 & -x_1 + x_2 & 0 \\
-Vz_1 + Vz_2 & 0 & Vx_1 - Vx_2 & z_1 - z_2 & 0 & -x_1 + x_2 \\
-Vy_2 + Vy_3 & Vx_2 - Vx_3 & 0 & y_2 - y_3 & -x_2 + x_3 & 0 \\
-Vz_2 + Vz_3 & 0 & Vx_2 - Vx_3 & z_2 - z_3 & 0 & -x_2 + x_3 \\
-Vy_3 + Vy_4 & Vx_3 - Vx_4 & 0 & y_3 - y_4 & -x_3 + x_4 & 0 \\
-Vz_3 + Vz_4 & 0 & Vx_3 - Vx_4 & z_3 - z_4 & 0 & -x_3 + x_4 \\
\end{pmatrix} \\
\text{and } b := \begin{pmatrix}
-x_1 \cdot Vy_1 + y_1 \cdot Vx_1 + x_2 \cdot Vy_2 - y_2 \cdot Vx_2 \\
-x_1 \cdot Vz_1 + z_1 \cdot Vx_1 + x_2 \cdot Vz_2 - z_2 \cdot Vx_2 \\
-x_2 \cdot Vy_2 + y_2 \cdot Vx_2 + x_3 \cdot Vy_3 - y_3 \cdot Vx_3 \\
-x_2 \cdot Vz_2 + z_2 \cdot Vx_2 + x_3 \cdot Vz_3 - z_3 \cdot Vx_3 \\
-x_3 \cdot Vy_3 + y_3 \cdot Vx_3 + x_4 \cdot Vy_4 - y_4 \cdot Vx_4 \\
-x_3 \cdot Vz_3 + z_3 \cdot Vx_3 + x_4 \cdot Vz_4 - z_4 \cdot Vx_4 \\
\end{pmatrix}.
$$
