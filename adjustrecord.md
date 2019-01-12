# 调参记录

## Step1：姿态重建参数调整

- **轮廓项对应代码及其可调节参数：**
  $$
  Esilh(θ) = G(woIrn(θ)C + wi(1 - Irn(θ))C¯ )
  $$
  对应于`step 1_pose.py line200`:

    ```python
    E = {
        'mask': gaussian_pyramid(rn_m * dist_o * 100. + (1 - rn_m) * dist_i, n_levels=4, normalization='size') * 80.,
        '2dpose': GMOf(frame.pose_obj, 100),
        'prior': frame.pose_prior_obj * 4.,
        'sp': frame.collision_obj * 1e3,
    }
    ```

​		这其中，mask中 的100. 对应于wo，这里wi为1。可调整wo与wi。

- **SMPL 构造项对应代码及可调节参数**：
  $$
  T (θ; β; D) = Tµ + Bs(β) + Bp(θ) + D
  $$
  对应于`step 1_pose.py line96-98 、106及117`

  ```python
  96:    weights = zip(
          [5., 4.5, 4.],
          [5., 4., 3.]
      )
      ...
  103:  for w_prior, w_betas in weights:
          x0 = [betas]
  
  106:    E = {
              'betas': E_betas * w_betas,
          }
  
          if E_height is not None:
              E['height'] = E_height
  
          for i, f in enumerate(frames):
              if np.sum(f.keypoints[[0, 2, 5, 8, 11], 2]) > 3.:
                  x0.extend([f.smpl.pose[range(21) + range(27, 30) + range(36, 60)], f.smpl.trans])
                  E['pose_{}'.format(i)] = f.pose_obj
  117:              E['prior_{}'.format(i)] = f.pose_prior_obj * w_prior
  ```

  96行中：weight 最终格式为：`[(5.,5.),(4.5,4.),(4.,3.)]` 元组中前一项为w_prior后一项为w_betas. 

  | 代码变量 | 含义             |
  | -------- | ---------------- |
  | w_prior  | 先验Pose的权重   |
  | w_betas  | 公式中Bs项的权重 |

- **帧选取相关参数：**

  在姿势重建的过程中，作者根据有效关节点数目对帧进行了过滤，为了获取更加精准的结果，可以调节选取的有效关节点以及数目进行优化：

  ```python
  if np.sum(f.keypoints[[0, 2, 5, 8, 11], 2]) > 3.:
  ```

  可以看到，作者选取了0,2,5,8,11这4个关键点，其置信度和大于3则视为有效帧，可以更改这个限制，调整有效帧选取来进行优化。

  ![COCO关节点示意图](https://ws1.sinaimg.cn/large/662f5c1fly1fxnug3i1atj20dc0hpt8q.jpg)

## Step2:共识姿态估计

- **能量项对应代码及其参数：**

  这一部分工作涉及到多个能量式，最终各个能量式向结合的权重是可调节的参数：
  $$
  Econs = Edata + wlpElp + wvarEvar + wsymEsym
  $$
  对应于`step 2_consensus.py line68~70`:

  ```python
  g_laplace = regularize_laplace()
  g_model = regularize_model()
  g_symmetry = regularize_symmetry()
  ...
  w_laplace *= g_laplace.reshape(-1, 1)
  w_model *= g_model.reshape(-1, 1)
  w_symmetry *= g_symmetry.reshape(-1, 1)
  ```

  可以看到 权重值最终来源于3个`regularize`函数。以下以其中一个举例：

  ```
  def regularize_laplace():
      reg = np.ones(6890)
      v_ids = get_bodypart_vertex_ids()
  
      reg[v_ids['face']] = 12.
      reg[v_ids['hand_l']] = 5.
      reg[v_ids['hand_r']] = 5.
      reg[v_ids['fingers_l']] = 8.
      reg[v_ids['fingers_r']] = 8.
      reg[v_ids['foot_l']] = 5.
      reg[v_ids['foot_r']] = 5.
      reg[v_ids['toes_l']] = 8.
      reg[v_ids['toes_r']] = 8.
      reg[v_ids['ear_l']] = 10.
      reg[v_ids['ear_r']] = 10.
  
      return reg
  ```

  可以看到他对于不同部分的边的正则值并不相同，根据对称原则修改参数可能带来优化。

