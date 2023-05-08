import os
#Directory containing downloaded files
download_dir = '/home/nhat/Documents/Distributed-Downloads'
# Rename each file in the directory
for i, filename in enumerate(os.listdir(download_dir)):
    if filename.endswith('.csv'):
        new_filename = f"{download_dir}/vInfectedHerdsOverTime_{i+1}.csv"
        old_filename = os.path.join(download_dir, filename)
        os.rename(old_filename, new_filename)
print(f"Rename Successfully!")