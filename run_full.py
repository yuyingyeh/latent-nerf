import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run script for texture inversion')
    parser.add_argument('--repo_root', default='/openroomssubstance/yyeh/latent-nerf')
    parser.add_argument('--concept_name', default='meta_chair2_multi')
    parser.add_argument('--init_token', default='chair')
    parser.add_argument('--shape_list', nargs='*', type=str, help='Input a list of shape names')
    args = parser.parse_args()

    # 1. If concept not exist, run texture inversion
    cmd = 'python3 sd_textual_inversion_training.py '
    cmd += '--concept_name %s ' % args.concept_name
    cmd += '--initializer_token %s ;' % args.init_token

    os.chdir(args.repo_root)
    print('>>> Running Command:')
    print(cmd)
    os.system(cmd)

    # 2. For each shape, run latent-paint
    # search for shape_path
    mesh_data_dir_list = [
        '/yyeh-data/threestudio/meshes/%s.obj',
        '/yyeh-data/3D-FUTURE/3D-FUTURE-model/%s/normalized_model.obj',
        # '/mnt/graphics_ssd/home/yyyeh/GitRepo/TEXTurePaper/shapes/%s.obj', 
        # '/mnt/graphics_ssd/home/yyyeh/GitRepo/threestudio/meshes/%s.obj',
        # '/mnt/graphics_ssd/home/yyyeh/data/scene_geometry/%s.obj', 
        # '/mnt/graphics_ssd/home/yyyeh/data/3D-FUTURE-model/%s/normalized_model.obj',
    ]
    mesh_id_dict = {'room_0': 'Mesh008', 
                    'bed_0': '02133f42-f8b1-4b10-9fe2-dec9a0bd1325',
                    'bed_1': '48d2dfa5-55dd-408f-a33b-4a085742e055',
                    'bed_2': '3f3e9fe3-3db0-407b-9956-57025c5b7e6d',
                    'bed_3': '647d9600-d011-409f-af3a-68afe22dd8cd',
                    'bed_4': '12b2dd21-c308-46e1-a375-471f67c2af77',
                    'bed_5': '0ab8bade-d500-4b65-ae65-020136a85d1e',
                    'sofa_0': 'f89da2db-ad8c-4582-b186-ed2a46f3cb15',
                    'sofa_1': '614ebd4c-9540-4ab0-85ff-0998020ce928',
                    'sofa_2': '3e08cbe7-87b9-45d6-80a4-0dfaee2b025c',
                    'sofa_3': 'ea720506-d8df-408c-a127-61b20b1a44b1',
                    'sofa_4': '517709cf-79a5-3309-af40-05e0c5ec992c',
                    'sofa_5': '1e71562b-34e3-44ac-b28e-d17589060ad0',
                    'sofa_6': '6132dd65-21cf-3e28-9ab3-4ea659d11be5',
                    'sofa_7': '592abfe3-905a-4d5b-98e7-f8d27568b531',
                    }
    if args.shape_list:
        for shape_name in args.shape_list:
            # /mnt/graphics_ssd/home/yyyeh/GitRepo/latent-nerf/experiments/toycat2teddy/results/step_05000_texture.png
            # /mnt/graphics_ssd/home/yyyeh/GitRepo/latent-nerf/experiments/toycat2teddy/results/imgs/step_05000_0000_rgb.png
            exp_name = '%s-as-%s' % (args.concept_name, shape_name)
            if os.path.exists(os.path.join(args.repo_root, 'experiments', exp_name, 'imgs/step_05000_0000_rgb.png')):
                print('Exp %s exists! Skip!' % exp_name)
                continue
            mesh_id = shape_name if shape_name not in mesh_id_dict.keys() else mesh_id_dict[shape_name]
            isExist = False
            for mesh_data_dir in mesh_data_dir_list:
                shape_path = mesh_data_dir % mesh_id
                if os.path.exists(shape_path):
                    isExist = True
                    break
            if not isExist:
                assert False

            # 2. Run latent-paint
            cmd = 'python3 -m scripts.train_latent_paint '
            cmd += '--log.exp_name %s ' % exp_name
            cmd += '--guide.text "A photo of %s object" ' % ('<sks>' if args.concept_name != 'toy-cat' else '<toy-cat>')
            cmd += '--guide.shape_path %s ' % shape_path
            cmd += '--guide.concept_name=%s' % args.concept_name
            
            os.chdir(args.repo_root)
            print('>>> Running Command:')
            print(cmd)
            os.system(cmd)

if __name__ == "__main__":
    main()