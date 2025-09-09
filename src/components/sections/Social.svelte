<script lang="ts">
    import Leaf from "../Leaf.svelte";
    import Load from "../Load.svelte";
</script>

<Leaf>
    <div class="flex flex-col w-full dodge-topbar px-8 gap-4">
        <Load until={true}>
            <h1 class="text-center px-15">
                Tính năng này chưa hoàn thiện trong bản MVP.
            </h1>
            <p>
                Chỉ có mockup cho tính năng này.
                <br />
                Đội thi đã vote để loại bỏ tính năng này ra khỏi ứng dụng MVP.
            </p>
        </Load>
    </div>
</Leaf>
