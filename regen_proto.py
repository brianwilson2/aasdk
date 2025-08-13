import os
import subprocess

# Change these to your project paths
PROTO_DIR = './aasdk_proto'       # folder with your .proto files
GEN_DIR = './build/aasdk_proto'  # folder where .pb.cc and .pb.h are generated

def clean_generated_files(gen_dir):
    print(f"Cleaning generated files in {gen_dir}...")
    for root, dirs, files in os.walk(gen_dir):
        for file in files:
            if file.endswith('.pb.cc') or file.endswith('.pb.h'):
                path = os.path.join(root, file)
                print(f"Removing {path}")
                os.remove(path)

def regenerate_proto(proto_dir, gen_dir):
    print(f"Regenerating protobuf files from {proto_dir} into {gen_dir}...")
    for file in os.listdir(proto_dir):
        if file.endswith('.proto'):
            proto_path = os.path.join(proto_dir, file)
            cmd = [
                "protoc",
                f"-I{proto_dir}",   # Add this line so protoc knows where to find imports
                f"--cpp_out={gen_dir}",
                os.path.join(proto_dir, file),
            ]
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)

if __name__ == "__main__":
    clean_generated_files(GEN_DIR)
    regenerate_proto(PROTO_DIR, GEN_DIR)
    print("Done!")
